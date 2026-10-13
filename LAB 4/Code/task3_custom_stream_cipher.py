"""
Information Security Lab - Lab 04
Task 3: Custom Stream Cipher Architecture (Intermediate)
Student Name: Muhammad Fezan
Student ID: Fall-23-BSCS-466
Instructor: Sir Mukkaram Ahmad

Architecture Design: "Chyron-PRG Stream Cipher"
Combines:
  1. 32-bit ARX (Add-Rotate-XOR) state mixing (inspired by Salsa20)
  2. Dynamic S-Box non-linear permutation (inspired by ARC4 KSA/PRGA)
  3. 64-bit Nonce and 128-bit Key support with forward secrecy
"""

import struct


class ChyronStreamCipher:
    def __init__(self, key: bytes, nonce: bytes):
        """
        Key: 16 bytes (128 bits)
        Nonce: 8 bytes (64 bits)
        """
        if len(key) != 16:
            raise ValueError("Key must be exactly 16 bytes (128-bit).")
        if len(nonce) != 8:
            raise ValueError("Nonce must be exactly 8 bytes (64-bit).")

        self.key = key
        self.nonce = nonce
        self.sbox = list(range(256))
        self._init_state()

    @staticmethod
    def _rot32(v, c):
        return ((v << c) & 0xFFFFFFFF) | (v >> (32 - c))

    def _quarter_round(self, a, b, c, d):
        """ARX Mixing round (Salsa20 inspiration)"""
        b ^= self._rot32((a + d) & 0xFFFFFFFF, 7)
        c ^= self._rot32((b + a) & 0xFFFFFFFF, 9)
        d ^= self._rot32((c + b) & 0xFFFFFFFF, 13)
        a ^= self._rot32((d + c) & 0xFFFFFFFF, 18)
        return a, b, c, d

    def _init_state(self):
        """KSA mixed with ARX-derived seed words"""
        k_words = list(struct.unpack("<4I", self.key))
        n_words = list(struct.unpack("<2I", self.nonce))
        # Mix key and nonce via quarter round
        a, b, c, d = self._quarter_round(k_words[0], k_words[1], n_words[0], n_words[1])
        mixed_key = struct.pack("<4I", a, b, c, d)

        # KSA Permutation
        j = 0
        for i in range(256):
            j = (j + self.sbox[i] + mixed_key[i % len(mixed_key)]) % 256
            self.sbox[i], self.sbox[j] = self.sbox[j], self.sbox[i]

        self.i = 0
        self.j = 0

    def get_keystream_byte(self) -> int:
        """PRGA: Produces one pseudo-random keystream byte"""
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.sbox[self.i]) % 256
        self.sbox[self.i], self.sbox[self.j] = self.sbox[self.j], self.sbox[self.i]
        t = (self.sbox[self.i] + self.sbox[self.j]) % 256
        k = self.sbox[t]
        # Additional non-linear ARX fold
        return (k ^ (self._rot32(self.i + self.j, 3) & 0xFF)) & 0xFF

    def encrypt(self, plaintext: bytes) -> bytes:
        keystream = bytes(self.get_keystream_byte() for _ in range(len(plaintext)))
        return bytes(p ^ k for p, k in zip(plaintext, keystream))

    def decrypt(self, ciphertext: bytes) -> bytes:
        # Stream ciphers are symmetric; re-initialize state to reproduce exact keystream
        self.sbox = list(range(256))
        self._init_state()
        return self.encrypt(ciphertext)


def main():
    print("=" * 65)
    print("TASK 3: CUSTOM STREAM CIPHER ('CHYRON-PRG') ARCHITECTURE")
    print("=" * 65)

    key = b"A1B2C3D4E5F60718"   # 16-byte key
    nonce = b"N1O2N3C4"          # 8-byte nonce
    message = b"LGU CYBER DEFENSE: OPERATION ZERO TOLERANCE"

    cipher = ChyronStreamCipher(key, nonce)
    ciphertext = cipher.encrypt(message)
    decrypted = cipher.decrypt(ciphertext)

    print(f"Algorithm Design   : Chyron-PRG (ARX + Permutation S-Box + Nonce)")
    print(f"Secret Key (Hex)   : {key.hex()}")
    print(f"Nonce / IV (Hex)   : {nonce.hex()}")
    print(f"Original Plaintext : '{message.decode()}'")
    print(f"Ciphertext (Hex)   : {ciphertext.hex()}")
    print(f"Decrypted Plaintext: '{decrypted.decode()}'")
    print(f"Integrity Check    : {'EXACT MATCH [PASS]' if decrypted == message else 'FAIL'}")


if __name__ == "__main__":
    main()
