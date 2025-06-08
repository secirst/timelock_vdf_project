import json
import time
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def legendre_symbol(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli_shanks(a, p):
    if legendre_symbol(a, p) != 1:
        return None
    if a == 0:
        return 0
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while legendre_symbol(z, p) != p - 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 1
        t2i = pow(t, 2, p)
        while t2i != 1 and i < m:
            t2i = pow(t2i, 2, p)
            i += 1
        if i == m:
            return None
        b = pow(c, 2 ** (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    return r

def mod_sqrt(a, p):
    root = tonelli_shanks(a, p)
    if root is None:
        return None, None
    return root, p - root

def vdf_invert(y, T, N):
    x_candidates = [y]
    for i in range(T):
        next_candidates = []
        for val in x_candidates:
            r1, r2 = mod_sqrt(val, N)
            if r1 is None:
                continue
            next_candidates.extend([r1, r2])
        x_candidates = next_candidates
    return x_candidates  # 可能有多个根

def time_lock_decrypt(broadcast_package):
    T = broadcast_package["T"]
    N = int(broadcast_package["N"])
    y = int(broadcast_package["vdf_y"])
    timestamp = broadcast_package.get("timestamp", 0)

    print("[*] Starting VDF inverse computation (this may take time)...")
    roots = vdf_invert(y, T, N)
    if not roots:
        raise ValueError("[!] Failed to compute modular square roots.")

    ciphertext = bytes.fromhex(broadcast_package["ciphertext"])
    iv = bytes.fromhex(broadcast_package["iv"])

    for idx, x in enumerate(roots):
        x_bytes = x.to_bytes((x.bit_length() + 7) // 8, 'big')
        aes_key = hashlib.sha256(x_bytes).digest()[:16]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        try:
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
            print(f"[+] Decryption succeeded with root #{idx + 1}")
            return plaintext
        except:
            continue

    raise ValueError("[!] All candidate roots failed. Decryption aborted.")

if __name__ == "__main__":
    with open("broadcast_package.json", "r") as f:
        package = json.load(f)
    secret = time_lock_decrypt(package)
    print(f"[Decryption Result] Plaintext message: {secret}")
