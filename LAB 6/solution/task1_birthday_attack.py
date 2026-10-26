#!/usr/bin/env python3
"""
Task 1 - Birthday Attack on a 16-bit Truncated SHA-256
Information Security Lab 06 (Secure Hash Functions)
Muhammad Fezan - Fall-23-BSCS-466

A hash of n bits has 2^n possible outputs. The birthday paradox says that a
collision appears after roughly sqrt(pi/2 * 2^n) random inputs, not 2^n.
For n = 16 that is about 321 messages, so the attack runs in milliseconds.

The program truncates SHA-256 to its first 16 bits and searches for two
DIFFERENT messages that produce the same 16-bit tag.
"""

import hashlib
import math
import os
import time

TRUNC_BITS = 16
TRUNC_BYTES = TRUNC_BITS // 8          # 2 bytes
SPACE = 1 << TRUNC_BITS                # 65,536 possible tags
TRIALS = 200


def sha256(msg: bytes) -> bytes:
    """Full 256-bit SHA-256 digest."""
    return hashlib.sha256(msg).digest()


def tag16(msg: bytes) -> bytes:
    """First 16 bits of the SHA-256 digest - the truncated hash."""
    return sha256(msg)[:TRUNC_BYTES]


def make_message(i: int) -> bytes:
    """Build a unique message: counter + 6 random bytes as nonce."""
    return f"LGU-IS-Lab06 | msg {i:07d} | nonce {os.urandom(6).hex()}".encode()


def find_collision(offset: int = 0):
    """Generate messages until two of them share the same 16-bit tag."""
    seen = {}
    n = 0
    while True:
        msg = make_message(offset + n)
        t = tag16(msg)
        n += 1
        if t in seen and seen[t] != msg:
            return seen[t], msg, n
        seen[t] = msg


def birthday_probability(n: int, space: int = SPACE) -> float:
    """P(at least one collision) after n draws from `space` values."""
    return 1.0 - math.exp(-n * (n - 1) / (2.0 * space))


def main():
    bar = "=" * 68
    print(bar)
    print(" TASK 1 : BIRTHDAY ATTACK - 16-BIT TRUNCATED SHA-256")
    print(bar)
    print(f"Hash function      : SHA-256 (FIPS 180-4)")
    print(f"Truncation         : first {TRUNC_BITS} bits ({TRUNC_BYTES} bytes)")
    print(f"Tag space          : 2^{TRUNC_BITS} = {SPACE:,} possible values")
    print(f"Birthday bound     : sqrt(pi/2 * 2^{TRUNC_BITS}) = "
          f"{math.sqrt(math.pi / 2 * SPACE):.1f} messages for 50% chance")
    print()

    # ---------------- single run ----------------
    print("-- Single run " + "-" * 54)
    t0 = time.perf_counter()
    a, b, n = find_collision()
    elapsed = (time.perf_counter() - t0) * 1000

    ha, hb = sha256(a), sha256(b)
    print(f"Message A          : {a.decode()}")
    print(f"SHA-256(A)         : {ha.hex()}")
    print(f"Truncated tag A    : {ha[:TRUNC_BYTES].hex()}")
    print()
    print(f"Message B          : {b.decode()}")
    print(f"SHA-256(B)         : {hb.hex()}")
    print(f"Truncated tag B    : {hb[:TRUNC_BYTES].hex()}")
    print()
    print(f"Messages generated : {n}")
    print(f"Collisions found   : 1")
    print(f"Time taken         : {elapsed:.2f} ms")
    print()
    print(f"A is different from B : {a != b}")
    print(f"Truncated tags equal  : {ha[:TRUNC_BYTES] == hb[:TRUNC_BYTES]}")
    print(f"Full hashes equal     : {ha == hb}")
    print(f"Collision probability : {birthday_probability(n) * 100:.2f}% "
          f"after {n} messages")
    print()

    # ---------------- repeated trials ----------------
    print(f"-- Statistics over {TRIALS} independent trials " + "-" * 22)
    counts = []
    for i in range(TRIALS):
        _, _, c = find_collision(offset=(i + 1) * 100_000)
        counts.append(c)

    counts.sort()
    mean = sum(counts) / len(counts)
    median = counts[len(counts) // 2]
    q1 = counts[len(counts) // 4]
    q3 = counts[3 * len(counts) // 4]
    sd = (sum((c - mean) ** 2 for c in counts) / (len(counts) - 1)) ** 0.5
    theory = math.sqrt(math.pi / 2 * SPACE)
    print(f"Minimum            : {counts[0]} messages")
    print(f"Q1 / median / Q3   : {q1} / {median} / {q3} messages")
    print(f"Maximum            : {counts[-1]} messages")
    print(f"Mean               : {mean:.1f} messages")
    print(f"Standard deviation : {sd:.1f} messages")
    print(f"Theoretical mean   : {theory:.1f} messages")
    print(f"Deviation          : {(mean - theory) / theory * 100:+.1f}%")
    print()

    # histogram in buckets of 100 messages
    print("Distribution (bucket = 100 messages)")
    buckets = {}
    for c in counts:
        buckets[(c - 1) // 100 * 100] = buckets.get((c - 1) // 100 * 100, 0) + 1
    for start in range(0, max(buckets) + 100, 100):
        cnt = buckets.get(start, 0)
        if cnt == 0 and start > max(buckets):
            break
        print(f"  {start:>4}-{start + 99:<4} {'#' * cnt} {cnt}")
    print()
    print(f"Half of all attacks succeed within {median} messages "
          f"({median / SPACE * 100:.1f}% of the tag space)")
    print(bar)


if __name__ == "__main__":
    main()
