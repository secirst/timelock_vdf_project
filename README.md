Timelock Broadcast Encryption System
A Python-based time-lock encryption system that allows broadcasting encrypted messages which can only be decrypted after a preset computational delay, enforced using a Verifiable Delay Function (VDF).

Table of Contents
Project Overview
Features
Prerequisites
Installation
Usage
How It Works
Configuration
Testing
Troubleshooting
Future Improvements
License

Project Overview
This project implements a time-lock broadcast encryption system in Python. It uses a **Verifiable Delay Function (VDF)** to delay access to a symmetric AES key. The encryption ensures that **receivers cannot decrypt the message until after performing a computational delay**, regardless of their system clock or intent.

Features
Time-lock encryption based on VDF + AES-CBC.
Enforced delay through repeated squaring (no trusted time server required).
Self-contained broadcast package with all decryption materials.
Command-line interface for message input and delay configuration.
Modular code structure for easy testing and enhancement.

Prerequisites
Python 3.7+
Required Python packages:
pycryptodome
Install packages with:
pip install pycryptodome

Installation
1.Clone or download this repository to your local machine.
2.Make sure Python 3 and required packages are installed.

Usage
Encrypt and Broadcast
Run the encryption script:
python encrypt_and_broadcast.py
You will be prompted to:
Enter the plaintext message to encrypt.
Enter the VDF difficulty parameter T (e.g., 20 for moderate delay).
A broadcast_package.json file will be generated.

Receive and Decrypt
Run the decryption script:
python receive_and_decrypt.py
This script:
Loads the broadcast package.
Performs T rounds of modular square root computation to recover the AES key.
Decrypts the message using AES.

How It Works
A random AES key is generated to encrypt the message using AES-CBC.
This AES key is then encoded as an integer x, and time-locked using the VDF:
y = x^(2^T) mod N
The broadcast package includes:
ciphertext, iv — for AES decryption
y, N, and T — to reconstruct x
Receivers perform T modular square root operations in reverse to recover x, derive the AES key as:
key = sha256(x_bytes)[:16]


Configuration
The RSA modulus N is stored in vdf_modulus.txt. You can replace it with any large prime or safe RSA modulus.
Parameter T controls the delay difficulty — higher T = longer decryption time.
AES encryption uses 128-bit CBC mode with PKCS7 padding.

Testing
You can run the correctness test:
python tests/test_correctness.py
This verifies the encryption-decryption cycle with sample parameters.

Troubleshooting
Padding errors during decryption: Ensure the correct AES key is derived and the ciphertext is not corrupted.
Module import errors: Check sys.path or run scripts from the project root directory.
Delay not respected: The delay is counted from broadcast generation time; ensure system clocks are synchronized if on different machines.

Future Improvements
Use AES-GCM (authenticated encryption)
Add digital signatures for authenticity
Allow time-locked file encryption
Optimize VDF using hardware acceleration or GPU
Use RSA composite modulus and avoid modular square root for strong delay enforcement

License
MIT License — see the LICENSE file for details.