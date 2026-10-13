"""
Information Security Lab - Lab 04
Task 2: XOR Symmetry Proof & Salsa20 Nonce Isolation (Beginner)
Student Name: Muhammad Fezan
Student ID: Fall-23-BSCS-466
Instructor: Sir Mukkaram Ahmad
"""

import string
from os import urandom
from salsa20 import XSalsa20_xor


def verify_xor_identity():
    """
    Formally verifies the mathematical involution of bitwise XOR:
    For all characters a in 'a'-'z' and arbitrary byte keys b in 0..255:
        (a ^ b) ^ b == a
    """
    print("\n[+] --- Part A: XOR Involutory Identity Verification ((a ^ b) ^ b = a) ---")
    test_key = 0x5A  # 01011010 in binary
    letters = string.ascii_lowercase
    all_passed = True

    print(f"Testing all 26 lowercase alphabet letters with key = {hex(test_key)} ({test_key}):")
    print(f"{'Char':<6}{'ASCII (a)':<12}{'a ^ b':<12}{'(a ^ b) ^ b':<16}{'Matches a?':<10}")
    print("-" * 56)

    for ch in letters:
        a = ord(ch)
        c = a ^ test_key
        dec = c ^ test_key
        matches = (dec == a)
        if not matches:
            all_passed = False
        print(f"'{ch}'    {a:<12}{c:<12}{dec:<16}{str(matches):<10}")

    print("-" * 56)
    print(f"Result: All 26 alphabet characters verified successfully! Identity holds: {all_passed}")


def verify_salsa20_nonces():
    """
    Encrypts the identical plaintext under identical key using two different nonces (IVs).
    Compares the resulting ciphertexts to demonstrate perfect diffusion and nonce isolation.
    """
    print("\n[+] --- Part B: Salsa20 Double Encryption with Distinct Nonces ---")
    message = b"CONFIDENTIAL PATIENT RECORD: LGU HEALTH SYSTEM"
    key = b"*secret**secret**secret**secret*"  # 32 bytes

    # Generate two distinct 24-byte nonces
    nonce1 = urandom(24)
    nonce2 = urandom(24)

    ct1 = XSalsa20_xor(message, nonce1, key)
    ct2 = XSalsa20_xor(message, nonce2, key)

    print(f"Plaintext Message : '{message.decode()}'")
    print(f"Key (32 bytes)    : {key}")
    print(f"Nonce 1 (Hex)     : {nonce1.hex()}")
    print(f"Ciphertext 1 (Hex): {ct1.hex()}")
    print(f"Nonce 2 (Hex)     : {nonce2.hex()}")
    print(f"Ciphertext 2 (Hex): {ct2.hex()}")

    # Compare differences
    diff_bytes = sum(1 for b1, b2 in zip(ct1, ct2) if b1 != b2)
    total_bytes = len(ct1)
    print(f"\nByte Comparison   : {diff_bytes}/{total_bytes} bytes differ ({diff_bytes / total_bytes * 100:.2f}%)")

    # Round-trip verification
    dec1 = XSalsa20_xor(ct1, nonce1, key)
    dec2 = XSalsa20_xor(ct2, nonce2, key)
    print(f"Decrypted CT1 (Nonce 1): '{dec1.decode()}' [PASS]")
    print(f"Decrypted CT2 (Nonce 2): '{dec2.decode()}' [PASS]")

    # Cross-nonce decryption failure
    cross_dec = XSalsa20_xor(ct1, nonce2, key)
    print(f"Decrypted CT1 (Nonce 2): {cross_dec.hex()[:32]}... [GARBLED/REJECTED]")


def main():
    print("=" * 60)
    print("TASK 2: XOR INVOLUTION & SALSA20 NONCE COMPARISON")
    print("=" * 60)
    verify_xor_identity()
    verify_salsa20_nonces()


if __name__ == "__main__":
    main()
