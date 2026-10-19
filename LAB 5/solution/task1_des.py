"""
Task 1 - DES Encryption and Decryption in ECB mode.
Course: Information Security (Lab) - Week 06
"""

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os


def generate_key():
    """Return a random 8-byte DES key."""
    return os.urandom(8)


def des_encrypt(key, plaintext):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, DES.block_size))


def des_decrypt(key, ciphertext):
    cipher = DES.new(key, DES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), DES.block_size)


if __name__ == "__main__":
    key = generate_key()
    plaintext = b"Lahore Garrison University - DES ECB demo block cipher lab."

    print("=" * 68)
    print(" TASK 1 : DES ENCRYPTION / DECRYPTION (ECB MODE)")
    print("=" * 68)
    print(f"Key (8 bytes, hex) : {key.hex()}")
    print(f"Key length         : {len(key) * 8} bits")
    print()
    print(f"Original plaintext : {plaintext.decode()}")
    print(f"Plaintext bytes    : {plaintext.hex()}")
    print(f"Plaintext length   : {len(plaintext)} bytes")
    print()

    ciphertext = des_encrypt(key, plaintext)
    print(f"Ciphertext (hex)   : {ciphertext.hex()}")
    print(f"Ciphertext length  : {len(ciphertext)} bytes "
          f"({len(ciphertext) // DES.block_size} blocks of 8 bytes)")
    print()

    recovered = des_decrypt(key, ciphertext)
    print(f"Decrypted plaintext: {recovered.decode()}")
    print(f"Decrypted bytes    : {recovered.hex()}")
    print()
    print(f"Match with original: {recovered == plaintext}")
    print("=" * 68)
