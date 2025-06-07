from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets

def generate_aes_key(key_size=16):
    """生成随机 AES 密钥，默认16字节（128位）"""
    return secrets.token_bytes(key_size)

def encrypt_aes(plaintext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(plaintext, AES.block_size))
    return cipher.iv + ct

def decrypt_aes(ciphertext: bytes, key: bytes) -> bytes:
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)
