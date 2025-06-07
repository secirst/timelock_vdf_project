import json
import time
import hashlib
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# VDF 计算

def vdf_eval(x, T, N):
    result = x
    for _ in range(T):
        result = pow(result, 2, N)
    return result

class VDFWorker(threading.Thread):
    def __init__(self, x, T, N):
        super().__init__()
        self.x = x
        self.T = T
        self.N = N
        self.result = None

    def run(self):
        print("[*] VDF computation started in background...")
        self.result = vdf_eval(self.x, self.T, self.N)
        print("[*] VDF computation completed.")

def time_lock_decrypt(broadcast_package):
    delay = broadcast_package["delay_seconds"]
    T = broadcast_package["T"]
    N = int(broadcast_package["N"])
    timestamp = broadcast_package.get("timestamp", 0)
    vdf_x_expected = int(broadcast_package["vdf_x"])

    # VDF初始x
    x = int.from_bytes(bytes.fromhex(broadcast_package["aes_key_hint"]), byteorder='big')

    # 开始计算VDF
    vdf_thread = VDFWorker(x, T, N)
    vdf_thread.start()

    # 等待到运行时间达到 timestamp + delay
    now = int(time.time())
    target_time = timestamp + delay
    wait_time = max(0, target_time - now)

    if wait_time > 0:
        print(f"[+] Waiting {wait_time} seconds until unlock time...")
        time.sleep(wait_time)
    else:
        print("[+] Unlock time already passed, just wait for VDF to finish.")

    print("[+] Waiting for VDF thread to complete...")
    vdf_thread.join()
    vdf_x = vdf_thread.result

    if vdf_x != vdf_x_expected:
        raise ValueError("[!] VDF output mismatch. Decryption aborted.")

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
