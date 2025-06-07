Timelock Broadcast Encryption System
A Python-based time-lock encryption system that allows broadcasting encrypted messages which can only be decrypted after a preset time delay, based on Verifiable Delay Function (VDF).

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
Acknowledgements

Project Overview
This project implements a timelock broadcast encryption system in Python, leveraging a Verifiable Delay Function (VDF) to encapsulate AES encryption keys. It ensures that messages can only be decrypted after a specified delay, regardless of when the decryption process starts.

Features
Time-lock encryption based on VDF and AES-CBC encryption.
Broadcast package generation with embedded delay parameters.
Secure decryption only possible after the time delay.
Command-line interactive input for message and delay configuration.
Modular code structure for easy maintenance and extension.

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
Enter the message to encrypt and broadcast.
Enter the delay time in seconds (e.g., 600 for 10 minutes).
Enter the VDF parameter T controlling the time-lock difficulty.
This creates a broadcast_package.json file.

Receive and Decrypt
Run the decryption script:
python receive_and_decrypt.py
The script reads broadcast_package.json, waits the specified delay, then performs the VDF calculation to unlock the AES key and decrypt the message.

How It Works
The plaintext message is encrypted using AES-CBC with a random AES key.
The AES key is then time-locked via repeated squaring in a large RSA modulus (N), acting as a Verifiable Delay Function.
The broadcast package stores the ciphertext, IV, encrypted key representation (vdf_x), modulus N, and delay parameters.
The receiver waits for the delay time and recomputes the VDF to retrieve the AES key, then decrypts the message.

Configuration
The RSA modulus N is stored in vdf_modulus.txt. You can replace it with a securely generated large prime or RSA modulus.
VDF parameter T controls delay complexity — larger values increase security but also computation time.
AES uses 128-bit key in CBC mode.

Testing
You can run the correctness test:
python tests/test_correctness.py
This verifies the encryption-decryption cycle with sample parameters.

Troubleshooting
Padding errors during decryption: Ensure the correct AES key is derived and the ciphertext is not corrupted.
Module import errors: Check sys.path or run scripts from the project root directory.
Delay not respected: The delay is counted from broadcast generation time; ensure system clocks are synchronized if on different machines.

Future Improvements
Use AES-GCM or authenticated encryption modes.
Add network broadcast and receiver modules.
Implement key integrity checks and digital signatures.
Support batch messages and more flexible scheduling.
Optimize VDF computation using dedicated libraries or hardware acceleration.

License
MIT License — see the LICENSE file for details.