import json
import os
import sys

# 设置项目根目录路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from encrypt_and_broadcast import time_lock_encrypt
from receive_and_decrypt import time_lock_decrypt

def test_encrypt_decrypt():
    msg = "Test message 123"
    T = 10  # 控制解密延迟的 VDF 参数
    package = time_lock_encrypt(msg, T)
    decrypted = time_lock_decrypt(package)
    assert decrypted == msg
    print("[✓] Test passed: Encryption and decryption succeeded.")

if __name__ == "__main__":
    test_encrypt_decrypt()
