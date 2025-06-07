import json
import time
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

# VDF计算函数，使用重复平方模N
def vdf_eval(x, T, N):
    result = x
    for _ in range(T):
        result = pow(result, 2, N)
    return result

# 从文件加载大素数模数N，文件内容应是16进制字符串（无0x前缀）
def load_modulus(filename="vdf_modulus.txt"):
    with open(filename, "r") as f:
        hex_str = f.read().strip()
        N = int(hex_str, 16)
    print("[*] Loaded modulus N from file.")
    return N

def time_lock_encrypt(message, delay_seconds, T):
    N = load_modulus()
    aes_key = get_random_bytes(16)

    x = int.from_bytes(aes_key, 'big')
    vdf_x = vdf_eval(x, T, N)

    vdf_x_bytes = vdf_x.to_bytes((vdf_x.bit_length() + 7) // 8, byteorder='big')
    derived_key = hashlib.sha256(vdf_x_bytes).digest()[:16]

    cipher = AES.new(derived_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))

    timestamp = int(time.time())  # 当前UTC时间戳，单位秒

    broadcast_package = {
        "ciphertext": ct_bytes.hex(),
        "iv": cipher.iv.hex(),
        "vdf_x": str(vdf_x),
        "N": str(N),
        "T": T,
        "delay_seconds": delay_seconds,
        "timestamp": timestamp,  # 新增字段，发布时间
    }

    with open("broadcast_package.json", "w") as f:
        json.dump(broadcast_package, f)
    print(f"[+] Broadcast package saved as broadcast_package.json")
    return broadcast_package


if __name__ == "__main__":
    print("===== Timelock Broadcast Encryption System =====")
    msg = input("Enter the message to encrypt and broadcast later: ")
    delay = int(input("Enter delay time in seconds (trusted delay before decryption): "))
    T = int(input("Enter VDF parameter T (e.g., 1000): "))
    time_lock_encrypt(msg, delay, T)
