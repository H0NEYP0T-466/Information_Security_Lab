"""
Task 2 - Meet-in-the-Middle (MITM) attack against Double DES.
Working demonstration on a scaled-down keyspace so it finishes in seconds.

Double DES:  C = E(k2, E(k1, P))

The attack is NOT a brute force over 2^(2k). It builds a lookup table on the
plaintext side and a probe on the ciphertext side, meeting at the intermediate
value, which costs 2 * 2^k operations instead of 2^(2k).
"""

import time
from Crypto.Cipher import DES

BLOCK = 8
BITS_PER_HALF = 14                  # 7 varying bits in each of 2 key bytes


def key_from_int(n):
    """
    Build an 8-byte DES key from a 14-bit counter.

    Only bits 2..8 of the last two bytes are used, because DES discards the
    least significant (parity) bit of every key byte. If the counter were
    spread over parity positions, several counters would collapse onto the
    same effective key and the recovered value would look wrong.
    """
    hi = (n >> 7) & 0x7F
    lo = n & 0x7F
    return bytes([0, 0, 0, 0, 0, 0, hi << 1, lo << 1])


def double_encrypt(p, k1, k2):
    return DES.new(k2, DES.MODE_ECB).encrypt(
        DES.new(k1, DES.MODE_ECB).encrypt(p))


def mitm_attack(plaintext, ciphertext, kspace):
    """
    Forward phase : table { E(k1, P) : k1 } for every k1    -> 2^k work + memory
    Backward phase: compute D(k2, C) and probe the table    -> 2^k work
    Match         : E(k1,P) == D(k2,C)  =>  C = E(k2, E(k1, P))
    """
    table = {}
    t0 = time.perf_counter()
    for i in range(kspace):
        table[DES.new(key_from_int(i), DES.MODE_ECB).encrypt(plaintext)] = i
    t_forward = time.perf_counter() - t0

    t0 = time.perf_counter()
    for j in range(kspace):
        mid = DES.new(key_from_int(j), DES.MODE_ECB).decrypt(ciphertext)
        if mid in table:
            return table[mid], j, len(table), t_forward, time.perf_counter() - t0
    return None, None, len(table), t_forward, time.perf_counter() - t0


if __name__ == "__main__":
    K1_SECRET, K2_SECRET = 0x0A2B, 0x1C4D
    KSPACE = 1 << BITS_PER_HALF      # 16,384 candidate keys per half

    plaintext = b"MITM-DEM"[:BLOCK]
    c1 = DES.new(key_from_int(K1_SECRET), DES.MODE_ECB).encrypt(plaintext)
    ciphertext = DES.new(key_from_int(K2_SECRET), DES.MODE_ECB).encrypt(c1)

    print("=" * 68)
    print(" TASK 2 : MEET-IN-THE-MIDDLE ATTACK ON DOUBLE DES")
    print("=" * 68)
    print(f"Plaintext  P        : {plaintext.decode()}  ({plaintext.hex()})")
    print(f"Secret K1           : {K1_SECRET:#06x}")
    print(f"Secret K2           : {K2_SECRET:#06x}")
    print(f"Intermediate E(K1,P): {c1.hex()}")
    print(f"Ciphertext C        : {ciphertext.hex()}")
    print()
    print(f"Effective keyspace  : 2^{BITS_PER_HALF} = {KSPACE:,} keys per half")
    print(f"Brute force (2DES)  : 2^{2 * BITS_PER_HALF} = {KSPACE ** 2:,} operations")
    print(f"MITM (2 x 2^{BITS_PER_HALF})    : {2 * KSPACE:,} operations")
    print(f"Speed-up factor     : {KSPACE // 2:,}x")
    print()

    k1, k2, entries, tf, tb = mitm_attack(plaintext, ciphertext, KSPACE)
    print(f"Forward table built : {entries:,} entries in {tf * 1000:.1f} ms")
    print(f"Backward search     : {tb * 1000:.1f} ms")
    print(f"Total attack time   : {(tf + tb):.2f} s")
    print()
    print(f"Recovered K1        : {k1:#06x}  -> match: {k1 == K1_SECRET}")
    print(f"Recovered K2        : {k2:#06x}  -> match: {k2 == K2_SECRET}")
    print()

    forged = double_encrypt(plaintext, key_from_int(k1), key_from_int(k2))
    print(f"Re-encrypt with k1,k2 : {forged.hex()}")
    print(f"Original ciphertext   : {ciphertext.hex()}")
    print(f"Attack successful     : {forged == ciphertext}")
    print("=" * 68)
