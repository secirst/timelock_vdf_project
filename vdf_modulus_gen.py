from Crypto.Util import number

def generate_large_prime(bits=2048):
    print("[*] Generating a large prime number...")
    prime = number.getPrime(bits)
    print("[*] Large prime generated.")
    return prime

def save_prime_to_file(prime, filename="vdf_modulus.txt"):
    with open(filename, "w") as f:
        f.write(hex(prime)[2:])
    print(f"[*] Prime saved to {filename}")

if __name__ == "__main__":
    N = generate_large_prime()
    save_prime_to_file(N)
