"""
Information Security Lab - Lab 04
Task 4: Adversarial Cryptanalysis Attacks on Custom Stream Cipher (Challenge)
Student Name: Muhammad Fezan
Student ID: Fall-23-BSCS-466
Instructor: Sir Mukkaram Ahmad

Attacks Implemented:
  1. Two-Time Pad (Keystream Reuse) Attack (C1 ^ C2 = P1 ^ P2)
  2. Active Bit-Flipping (Malleability) Attack on Unauthenticated Stream Cipher
"""

from task3_custom_stream_cipher import ChyronStreamCipher


def attack_keystream_reuse():
    print("\n[+] --- Attack 1: Two-Time Pad / Keystream Reuse Attack ---")
    shared_key = b"A1B2C3D4E5F60718"
    reused_nonce = b"STATIC01"

    # Victim sends two different messages under identical (key, nonce)
    p1 = b"ATTACK THE NORTH RIDGE AT DAWN!"
    p2 = b"DEFEND THE SOUTH PASS AT NOON!"

    c1 = ChyronStreamCipher(shared_key, reused_nonce).encrypt(p1)
    c2 = ChyronStreamCipher(shared_key, reused_nonce).encrypt(p2)

    # Adversary intercepts c1 and c2. Computes XOR difference:
    c_xor = bytes(b1 ^ b2 for b1, b2 in zip(c1, c2))
    p_xor = bytes(b1 ^ b2 for b1, b2 in zip(p1, p2))

    print(f"Plaintext 1       : {p1.decode()}")
    print(f"Plaintext 2       : {p2.decode()}")
    print(f"Ciphertext 1 (Hex): {c1.hex()[:40]}...")
    print(f"Ciphertext 2 (Hex): {c2.hex()[:40]}...")
    print(f"C1 XOR C2 matches P1 XOR P2? : {c_xor == p_xor} [TRUE]")

    # Adversary knows or guesses a crib from P1: "ATTACK"
    crib = b"ATTACK"
    recovered_p2_crib = bytes(c ^ k for c, k in zip(c_xor[:len(crib)], crib))
    print(f"Adversary Crib    : '{crib.decode()}'")
    print(f"Recovered P2 Piece: '{recovered_p2_crib.decode()}' (Exact match to P2 prefix!)")
    print("Vulnerability     : Because keystreams canceled out completely, knowing partial text")
    print("                    in message 1 instantly reveals the corresponding text in message 2.")


def attack_bit_flipping_malleability():
    print("\n[+] --- Attack 2: Active Bit-Flipping (Malleability) Attack ---")
    key = b"A1B2C3D4E5F60718"
    nonce = b"SESSION9"

    original_message = b"TRANSFER $0100 TO ALICE"
    cipher = ChyronStreamCipher(key, nonce)
    ciphertext = bytearray(cipher.encrypt(original_message))

    print(f"Original Transaction : '{original_message.decode()}'")
    print(f"Intercepted Ciphertext: {bytes(ciphertext).hex()}")

    # Adversary intercepts ciphertext in transit.
    # Wants to tamper $0100 -> $9900 without knowing the key!
    # Formula: C'[idx] = C[idx] ^ P[idx] ^ P_target[idx]
    target_patch = b"9900"
    start_idx = original_message.index(b"0100")

    for i, target_char in enumerate(target_patch):
        orig_char = original_message[start_idx + i]
        diff = orig_char ^ target_char
        ciphertext[start_idx + i] ^= diff  # Flip bits in ciphertext

    # Bank decrypts the tampered ciphertext with legitimate key
    tampered_plaintext = ChyronStreamCipher(key, nonce).decrypt(bytes(ciphertext))
    print(f"Tampered Ciphertext   : {bytes(ciphertext).hex()}")
    print(f"Decrypted at Bank     : '{tampered_plaintext.decode()}' [TAMPER SUCCESSFUL!]")
    print("Vulnerability         : Unauthenticated stream ciphers lack ciphertext integrity.")
    print("                        Mitigation: Must combine with MAC (e.g. Poly1305 / HMAC).")


def main():
    print("=" * 65)
    print("TASK 4: ADVERSARIAL ATTACKS (REUSE & BIT-FLIPPING)")
    print("=" * 65)
    attack_keystream_reuse()
    attack_bit_flipping_malleability()


if __name__ == "__main__":
    main()
