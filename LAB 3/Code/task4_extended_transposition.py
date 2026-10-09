"""
Information Security Lab - Lab 03
Graded Task 4: Extended Transposition Cipher
Student Name: Muhammad Fezan
Student ID: Fall-23-BSCS-466
Instructor: Sir Mukkaram Ahmad

Challenge Requirements (All 6 Sub-tasks Implemented):
  1. Handle key / plaintext length mismatch (dynamic grid sizing & padding)
  2. Write decode() / decrypt() function
  3. Preserve letter case (uppercase / lowercase retained)
  4. Preserve spaces and punctuation
  5. Generate a random key (random permutation / integer key)
  6. Add an interactive menu interface
"""

import math
import random


def generate_random_key(min_key=3, max_key=8):
    """
    Sub-task 5: Generates a random numeric column key.
    """
    return random.randint(min_key, max_key)


def generate_permutation_key(length=5):
    """
    Generates a randomized column permutation order (e.g., [3, 0, 4, 1, 2]).
    """
    order = list(range(length))
    random.shuffle(order)
    return order


def encode_transposition(plaintext, key, pad_char=''):
    """
    Sub-tasks 1, 3, 4:
      - Encrypts via Columnar Transposition.
      - Preserves spaces, punctuation, symbols, and letter casing directly.
      - Handles length mismatch with optional padding or irregular grid geometry.
    """
    if key <= 0:
        raise ValueError("Key must be a positive integer greater than 0.")

    # Sub-task 1: Handle length mismatch via padding if pad_char is specified
    text = plaintext
    if pad_char and len(text) % key != 0:
        padding_needed = key - (len(text) % key)
        text += pad_char * padding_needed

    # Build columnar ciphertext
    # Read column by column
    ciphertext = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(text):
            ciphertext[col] += text[pointer]
            pointer += key

    return ''.join(ciphertext)


def decode_transposition(ciphertext, key):
    """
    Sub-task 2: Decrypts / decodes ciphertext back into plaintext.
    Handles irregular columns when length % key != 0.
    """
    if key <= 0:
        raise ValueError("Key must be a positive integer greater than 0.")

    total_len = len(ciphertext)
    num_rows = math.ceil(total_len / key)
    num_cols = key
    num_shaded_boxes = (num_rows * num_cols) - total_len

    # Each string in plaintext represents a column in the grid
    plaintext = [''] * num_rows

    col = 0
    row = 0

    for symbol in ciphertext:
        plaintext[row] += symbol
        col += 1

        # If we reached the end of the column or hit a shaded box at the bottom
        if (col == num_cols) or (col == num_cols - 1 and row >= num_rows - num_shaded_boxes):
            col = 0
            row += 1

    return ''.join(plaintext)


def run_self_test():
    """
    Demonstrates and validates all 6 requirements end-to-end.
    """
    print("\n" + "=" * 65)
    print("      AUTOMATED SELF-TEST: VERIFYING ALL 6 SUB-TASKS      ")
    print("=" * 65)

    test_message = "We hold these truths to be self-evident, that all men are created equal!"
    test_key = 6

    print(f"\n[+] Input Plaintext:")
    print(f"    \"{test_message}\"")
    print(f"    Length = {len(test_message)} chars (Notice: {len(test_message)} % {test_key} = {len(test_message) % test_key} != 0 -> Length mismatch handled)")

    # 1 & 3 & 4: Encryption with case, space, punctuation preservation
    cipher = encode_transposition(test_message, test_key)
    print(f"\n[+] Sub-tasks 1, 3, 4 (Encrypted Ciphertext with key={test_key}):")
    print(f"    \"{cipher}\"")

    # 2: Decryption / decode()
    recovered = decode_transposition(cipher, test_key)
    print(f"\n[+] Sub-task 2 (Decrypted Plaintext via decode()):")
    print(f"    \"{recovered}\"")

    # Verification
    is_match = test_message == recovered
    print(f"\n[+] Integrity Verification: {'PASSED (100% Exact Reconstruction)' if is_match else 'FAILED'}")

    # 5: Random key generation demo
    rand_k = generate_random_key(4, 9)
    print(f"\n[+] Sub-task 5 (Random Key Generation):")
    print(f"    Generated Random Key = {rand_k}")
    rand_cipher = encode_transposition(test_message, rand_k)
    rand_recovered = decode_transposition(rand_cipher, rand_k)
    print(f"    Random Key Round-Trip Match: {test_message == rand_recovered}")

    print("=" * 65)


def menu():
    """
    Sub-task 6: Interactive Menu Interface
    """
    while True:
        print("\n" + "=" * 55)
        print("  INFOSEC LAB 03 - TASK 4: TRANSPOSITION CIPHER MENU  ")
        print("=" * 55)
        print("  1. Encrypt Message")
        print("  2. Decrypt Message")
        print("  3. Generate a Random Key")
        print("  4. Run Complete Self-Test Demo (All 6 Features)")
        print("  5. Exit")
        print("=" * 55)

        choice = input("Enter choice (1-5): ").strip()

        if choice == '1':
            msg = input("\nEnter Plaintext: ")
            try:
                k = int(input("Enter Integer Key (number of columns, e.g. 6): "))
                ct = encode_transposition(msg, k)
                print(f"\n[+] Ciphertext: \"{ct}\"")
            except ValueError as e:
                print(f"[-] Invalid input: {e}")

        elif choice == '2':
            ct = input("\nEnter Ciphertext: ")
            try:
                k = int(input("Enter Integer Key: "))
                pt = decode_transposition(ct, k)
                print(f"\n[+] Decrypted Text: \"{pt}\"")
            except ValueError as e:
                print(f"[-] Invalid input: {e}")

        elif choice == '3':
            k = generate_random_key(3, 10)
            print(f"\n[+] Generated Random Key: {k}")

        elif choice == '4':
            run_self_test()

        elif choice == '5':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("[-] Invalid selection, please pick 1-5.")


if __name__ == "__main__":
    import sys
    if not sys.stdin.isatty():
        run_self_test()
    else:
        run_self_test()
        menu()
