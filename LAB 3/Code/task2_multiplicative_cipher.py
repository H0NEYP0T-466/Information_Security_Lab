"""
Information Security Lab - Lab 03
Graded Task 2: Multiplicative Cipher & Cryptanalysis (Hacking It)
Student Name: Muhammad Fezan
Student ID: Fall-23-BSCS-466
Instructor: Sir Mukkaram Ahmad

Description:
  1. Multiplicative Cipher: A monoalphabetic substitution cipher where each
     letter index x (0-25) is encrypted as:
         C = (x * key) mod 26
     and decrypted as:
         P = (C * key_inv) mod 26
     where gcd(key, 26) == 1. Here, key = 7.
     Since 7 * 15 = 105 = 1 (mod 26), key_inv = 15.

  2. Cryptanalysis (Hacking the Cipher):
     - Vulnerability 1 (Tiny Key Space): Only 12 numbers in [0, 25] are coprime
       to 26. An attacker can brute-force all 12 keys in microseconds.
     - Vulnerability 2 (Frequency Analysis): Since it is monoalphabetic, the most
       frequent ciphertext character corresponds to the most frequent English
       letter ('E' = index 4).
"""

import math
from collections import Counter

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
M = 26
VALID_KEYS = [k for k in range(1, M) if math.gcd(k, M) == 1]  # 12 valid coprime keys


def mod_inverse(a, m=26):
    """Computes modular multiplicative inverse of a mod m."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def encrypt_multiplicative(plaintext, key=7):
    """
    Encrypts plaintext using C = (x * key) mod 26.
    Preserves casing and non-alphabetic characters.
    """
    if math.gcd(key, M) != 1:
        raise ValueError(f"Key {key} is invalid! Must be coprime to {M}.")

    ciphertext = []
    for char in plaintext:
        if char.isalpha():
            is_upper = char.isupper()
            x = ALPHABET.index(char.lower())
            cipher_idx = (x * key) % M
            c = ALPHABET[cipher_idx]
            ciphertext.append(c.upper() if is_upper else c)
        else:
            ciphertext.append(char)
    return ''.join(ciphertext)


def decrypt_multiplicative(ciphertext, key=7):
    """
    Decrypts ciphertext using P = (C * key_inv) mod 26.
    """
    key_inv = mod_inverse(key, M)
    if key_inv is None:
        raise ValueError(f"Key {key} has no modular inverse mod {M}!")

    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            is_upper = char.isupper()
            y = ALPHABET.index(char.lower())
            plain_idx = (y * key_inv) % M
            p = ALPHABET[plain_idx]
            plaintext.append(p.upper() if is_upper else p)
        else:
            plaintext.append(char)
    return ''.join(plaintext)


def attack_brute_force(ciphertext):
    """
    Hacks the multiplicative cipher via exhaustive search.
    Because gcd(key, 26) must be 1, there are only 12 possible keys in total:
    [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25].
    """
    print("\n" + "-" * 65)
    print("  [HACK METHOD 1: EXHAUSTIVE BRUTE-FORCE CRYPTANALYSIS]  ")
    print("-" * 65)
    print(f"Total possible coprime keys: {len(VALID_KEYS)} -> {VALID_KEYS}\n")

    results = []
    for candidate_key in VALID_KEYS:
        candidate_inv = mod_inverse(candidate_key, M)
        decrypted_attempt = decrypt_multiplicative(ciphertext, candidate_key)
        results.append((candidate_key, candidate_inv, decrypted_attempt))
        print(f"[*] Trying Key = {candidate_key:2d} (inv={candidate_inv:2d}) -> \"{decrypted_attempt[:60]}...\"")

    return results


def attack_frequency_analysis(ciphertext):
    """
    Hacks the multiplicative cipher using letter frequency.
    In English, 'E' (index 4) is the most frequent letter (~12.7%).
    If ciphertext letter C_max maps to 'E', then:
        (4 * key) mod 26 = C_max
    We can solve for candidate keys directly.
    """
    print("\n" + "-" * 65)
    print("  [HACK METHOD 2: STATISTICAL FREQUENCY ANALYSIS]  ")
    print("-" * 65)

    letters_only = [c.lower() for c in ciphertext if c.isalpha()]
    if not letters_only:
        print("[-] Insufficient alphabetic characters for frequency analysis.")
        return

    counts = Counter(letters_only)
    most_common_char, freq = counts.most_common(1)[0]
    c_idx = ALPHABET.index(most_common_char)

    print(f"[*] Most frequent ciphertext letter: '{most_common_char.upper()}' (count = {freq})")
    print(f"[*] Assuming '{most_common_char.upper()}' corresponds to English plaintext 'E' (index 4):")
    print(f"    Equation: (4 * key) mod 26 = {c_idx}")

    # Solve: 4 * k = c_idx (mod 26)
    candidate_keys = []
    for k in VALID_KEYS:
        if (4 * k) % M == c_idx:
            candidate_keys.append(k)

    print(f"[*] Deduce matching coprime key(s): {candidate_keys}")
    for k in candidate_keys:
        dec = decrypt_multiplicative(ciphertext, k)
        print(f"    -> Decryption with key {k}: \"{dec[:60]}...\"")


def main():
    print("=" * 65)
    print("   INFOSEC LAB 03 - TASK 2: MULTIPLICATIVE CIPHER & HACKING IT   ")
    print("=" * 65)

    key = 7
    key_inv = mod_inverse(key, M)

    print(f"\n[+] Cipher Parameters:")
    print(f"    - Modulus: {M}")
    print(f"    - Multiplicative Key (k): {key}")
    print(f"    - Modular Multiplicative Inverse (k^-1 mod 26): {key_inv}")
    print(f"    - Verification: ({key} * {key_inv}) % 26 = {(key * key_inv) % 26}")

    sample_text = "We hold these truths to be self-evident, that all men are created equal."
    print(f"\n[1] Original Plaintext:")
    print(f"    \"{sample_text}\"")

    # 1. Encrypt
    cipher = encrypt_multiplicative(sample_text, key=key)
    print(f"\n[2] Encrypted Ciphertext (key = {key}):")
    print(f"    \"{cipher}\"")

    # 2. Decrypt
    decrypted = decrypt_multiplicative(cipher, key=key)
    print(f"\n[3] Decrypted Plaintext (key_inv = {key_inv}):")
    print(f"    \"{decrypted}\"")

    # 3. Demonstration of Hacking
    attack_brute_force(cipher)
    attack_frequency_analysis(cipher)

    print("\n" + "=" * 65)
    print("  CONCLUSION:")
    print("  The Multiplicative Cipher is trivially broken because:")
    print("  1. The key space has only 12 keys (brute force finishes instantly).")
    print("  2. It preserves single-letter frequency distributions.")
    print("=" * 65)


if __name__ == "__main__":
    main()
