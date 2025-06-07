from Crypto.Util import number

def generate_rsa_modulus(bits=2048):
    print("[*] Generating two large primes for RSA modulus N...")
    p = number.getPrime(bits // 2)
    q = number.getPrime(bits // 2)
    N = p * q
    print("[*] RSA modulus N generated.")
    return N

def save_modulus_to_file(N, filename="vdf_modulus.txt"):
    with open(filename, "w") as f:
        f.write(hex(N)[2:])  # 写入十六进制字符串，不带0x
    print(f"[*] Modulus saved to {filename}")

if __name__ == "__main__":
    N = generate_rsa_modulus()
    save_modulus_to_file(N)
