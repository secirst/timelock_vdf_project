import json
import time
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# VDF计算函数（重复平方模N），理想中接收端用VDF解密时要花时间，这里示例简单直接读取vdf_x
def vdf_eval(x, T, N):
    result = x
    for _ in range(T):
        result = pow(result, 2, N)
    return result

def time_lock_decrypt(broadcast_package):
    delay = broadcast_package["delay_seconds"]
    T = broadcast_package["T"]
    N = int(broadcast_package["N"])
    timestamp = broadcast_package.get("timestamp", 0)

    now = int(time.time())
    elapsed = now - timestamp
    wait_time = delay - elapsed

    if wait_time > 0:
        print(f"[+] Wait for {wait_time} seconds to meet the time lock condition...")
        time.sleep(wait_time)
    else:
        print("[+] Delay time already passed, start decrypting immediately.")

    print("[+] Calculate the VDF to unlock the AES key...")
    vdf_x = int(broadcast_package["vdf_x"])

    vdf_x_bytes = vdf_x.to_bytes((vdf_x.bit_length() + 7) // 8, byteorder='big')
    aes_key = hashlib.sha256(vdf_x_bytes).digest()[:16]

    ciphertext = bytes.fromhex(broadcast_package["ciphertext"])
    iv = bytes.fromhex(broadcast_package["iv"])

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    return plaintext


if __name__ == "__main__":
    filename = "broadcast_package.json"
    with open(filename, "r") as f:
        package = json.load(f)

    secret = time_lock_decrypt(package)
    print(f"[Decryption Result] Plaintext message: {secret}")
