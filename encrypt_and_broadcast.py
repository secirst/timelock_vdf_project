import json
import time
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def vdf_eval(x, T, N):
    result = x
    for _ in range(T):
        result = pow(result, 2, N)
    return result

def load_modulus(filename="vdf_modulus.txt"):
    with open(filename, "r") as f:
        hex_str = f.read().strip()
        N = int(hex_str, 16)
    print("[*] Loaded modulus N from file.")
    return N

def time_lock_encrypt(message, T):
    N = load_modulus()
    aes_key = get_random_bytes(16)
    x = int.from_bytes(aes_key, 'big')
    y = vdf_eval(x, T, N)

    x_bytes = aes_key
    derived_key = hashlib.sha256(x_bytes).digest()[:16]

    cipher = AES.new(derived_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))

    broadcast_package = {
        "ciphertext": ct_bytes.hex(),
        "iv": cipher.iv.hex(),
        "vdf_y": str(y),
        "N": str(N),
        "T": T,
    }

    with open("broadcast_package.json", "w") as f:
        json.dump(broadcast_package, f)
    print(f"[+] Broadcast package saved as broadcast_package.json")
    return broadcast_package

if __name__ == "__main__":
    print("===== Timelock Broadcast Encryption System =====")
    msg = input("Enter the message to encrypt and broadcast later: ")
    T = int(input("Enter VDF parameter T (e.g., 20): "))
    time_lock_encrypt(msg, T)
