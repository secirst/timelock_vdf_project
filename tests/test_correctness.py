import json
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from encrypt_and_broadcast import time_lock_encrypt
from receive_and_decrypt import time_lock_decrypt

def test_encrypt_decrypt():
    msg = "Test message 123"
    delay = 2
    T = 10
    package = time_lock_encrypt(msg, delay, T)
    decrypted = time_lock_decrypt(package)
    assert decrypted == msg
    print("Everything is OK.")

if __name__ == "__main__":
    test_encrypt_decrypt()
