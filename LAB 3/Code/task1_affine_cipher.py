"""
Information Security Lab - Lab 03
Graded Task 1: Affine Cipher (Encryption & Decryption)
Student Name: Muhammad Fezan
Student ID: Fall-23-BSCS-466
Instructor: Sir Mukkaram Ahmad

Description:
  The Affine Cipher is a monoalphabetic substitution cipher where each letter
  is mapped to its numerical equivalent, encrypted using the linear equation:
      C = (a * P + b) mod 26
  and decrypted using:
      P = a_inv * (C - b) mod 26
  where 'a' must be coprime to 26 (gcd(a, 26) = 1) and a_inv is the modular
  multiplicative inverse of 'a' modulo 26.
"""

import math

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
M = 26  # Symbol-set size (English alphabet)


def mod_inverse(a, m):
    """
    Finds the modular multiplicative inverse of a modulo m using
    the Extended Euclidean Algorithm.
    Returns x such that (a * x) % m == 1.
    """
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def encrypt_affine(plaintext, a, b):
    """
    Encrypts plaintext using the Affine Cipher: E(x) = (a * x + b) mod 26.
    Preserves casing, punctuation, spaces, and non-alphabet characters.
    """
    if math.gcd(a, M) != 1:
        raise ValueError(f"Key 'a' ({a}) must be coprime to {M} (gcd must be 1).")

    ciphertext = []
    for char in plaintext:
        if char.isalpha():
            is_upper = char.isupper()
            x = ALPHABET.index(char.lower())
            encrypted_idx = (a * x + b) % M
            cipher_char = ALPHABET[encrypted_idx]
            ciphertext.append(cipher_char.upper() if is_upper else cipher_char)
        else:
            # Preserve spaces, digits, punctuation
            ciphertext.append(char)

    return ''.join(ciphertext)


def decrypt_affine(ciphertext, a, b):
    """
    Decrypts ciphertext using: D(y) = a_inv * (y - b) mod 26.
    """
    a_inv = mod_inverse(a, M)
    if a_inv is None:
        raise ValueError(f"No modular inverse exists for key 'a' = {a} mod {M}.")

    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            is_upper = char.isupper()
            y = ALPHABET.index(char.lower())
            decrypted_idx = (a_inv * (y - b)) % M
            plain_char = ALPHABET[decrypted_idx]
            plaintext.append(plain_char.upper() if is_upper else plain_char)
        else:
            plaintext.append(char)

    return ''.join(plaintext)


def main():
    print("=" * 65)
    print("      INFOSEC LAB 03 - TASK 1: AFFINE CIPHER IMPLEMENTATION      ")
    print("=" * 65)

    # Key parameters
    key_a = 5
    key_b = 8
    
    print(f"\n[+] Configuration Parameters:")
    print(f"    - Modulus (m): {M}")
    print(f"    - Multiplicative Key (a): {key_a}  [gcd({key_a}, {M}) = {math.gcd(key_a, M)}]")
    print(f"    - Additive Shift Key (b): {key_b}")
    a_inv = mod_inverse(key_a, M)
    print(f"    - Modular Inverse of a (a^-1 mod 26): {a_inv}  (since {key_a} * {a_inv} = {key_a * a_inv} = 1 mod 26)")

    # Sample text from Lab 3 slide deck
    sample_text = "We hold these truths to be self-evident, that all men are created equal."
    print(f"\n[1] Original Plaintext:")
    print(f"    \"{sample_text}\"")

    # Encryption
    cipher = encrypt_affine(sample_text, key_a, key_b)
    print(f"\n[2] Encrypted Ciphertext:")
    print(f"    \"{cipher}\"")

    # Decryption
    decrypted = decrypt_affine(cipher, key_a, key_b)
    print(f"\n[3] Decrypted Plaintext:")
    print(f"    \"{decrypted}\"")

    # Verification
    is_valid = sample_text == decrypted
    print(f"\n[+] Verification Check: {'PASSED (100% Match)' if is_valid else 'FAILED'}")
    print("=" * 65)


if __name__ == "__main__":
    main()
