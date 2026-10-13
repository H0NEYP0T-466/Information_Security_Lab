"""
Information Security Lab - Lab 04
Task 1: ARC4 & Vernam Stream Ciphers (Beginner)
Student Name: Muhammad Fezan
Student ID: Fall-23-BSCS-466
Instructor: Sir Mukkaram Ahmad
"""

def arc4crypt(data, key):
    """
    ARC4 Stream Cipher implementation.
    KSA (Key-Scheduling Algorithm) initializes the permutation table.
    PRGA (Pseudo-Random Generation Algorithm) produces the keystream bytes.
    """
    x = 0
    box = list(range(256))
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]

    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        k = box[(box[x] + box[y]) % 256]
        out.append(chr(ord(char) ^ k))
    return ''.join(out)


def VernamEncDec(text, key):
    """
    Vernam Cipher implementation with repeating key pointer.
    Ciphertext = Plaintext XOR Key (bitwise).
    """
    result = ""
    ptr = 0
    for char in text:
        result += chr(ord(char) ^ ord(key[ptr]))
        ptr += 1
        if ptr == len(key):
            ptr = 0
    return result


def main():
    print("=" * 60)
    print("TASK 1: ARC4 & VERNAM STREAM CIPHERS VERIFICATION")
    print("=" * 60)

    # --- ARC4 Demonstration ---
    print("\n[+] --- ARC4 Cipher Demonstration ---")
    plaintext_arc4 = "Dive Dive Dive"
    correct_key_arc4 = "SuperSecretKey!!"
    wrong_key_arc4 = "WrongSecretKey!!"

    ciphertext_arc4 = arc4crypt(plaintext_arc4, correct_key_arc4)
    cipher_hex_arc4 = ciphertext_arc4.encode('latin-1').hex()
    decrypted_correct_arc4 = arc4crypt(ciphertext_arc4, correct_key_arc4)
    decrypted_wrong_arc4 = arc4crypt(ciphertext_arc4, wrong_key_arc4)

    print(f"Original Plaintext  : '{plaintext_arc4}'")
    print(f"Key Used            : '{correct_key_arc4}'")
    print(f"Ciphertext (Hex)    : {cipher_hex_arc4}")
    print(f"Decrypted (Correct) : '{decrypted_correct_arc4}'")
    print(f"Decrypted (Wrong)   : '{decrypted_wrong_arc4}' (Raw bytes: {decrypted_wrong_arc4.encode('latin-1', 'replace').hex()})")
    print("Observation         : Decrypting with an incorrect key yields pseudo-random garbled bytes")
    print("                      because the KSA generates a completely desynchronized keystream.")

    # --- Vernam Demonstration ---
    print("\n[+] --- Vernam Cipher Demonstration ---")
    plaintext_vernam = "Cryptographic protocols"
    correct_key_vernam = "thisismykey12345"
    wrong_key_vernam = "wrongismykey9999"

    ciphertext_vernam = VernamEncDec(plaintext_vernam, correct_key_vernam)
    cipher_hex_vernam = ciphertext_vernam.encode('latin-1').hex()
    decrypted_correct_vernam = VernamEncDec(ciphertext_vernam, correct_key_vernam)
    decrypted_wrong_vernam = VernamEncDec(ciphertext_vernam, wrong_key_vernam)

    print(f"Original Plaintext  : '{plaintext_vernam}'")
    print(f"Key Used            : '{correct_key_vernam}'")
    print(f"Ciphertext (Hex)    : {cipher_hex_vernam}")
    print(f"Decrypted (Correct) : '{decrypted_correct_vernam}'")
    print(f"Decrypted (Wrong)   : '{decrypted_wrong_vernam}'")
    print("Observation         : With Vernam, XORing with a wrong key corrupts character positions")
    print("                      directly proportional to the bit differences between keys (c ^ k2 = p ^ k1 ^ k2).")


if __name__ == "__main__":
    main()
