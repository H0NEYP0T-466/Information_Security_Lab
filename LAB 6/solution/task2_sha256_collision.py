#!/usr/bin/env python3
"""
Task 2 - SHA-256 Collision Detection on Complete Hashes
Information Security Lab 06 (Secure Hash Functions)
Muhammad Fezan - Fall-23-BSCS-466

The program hashes one million random messages with the FULL 256-bit SHA-256
and stores every digest in a dictionary, so a repeated digest is detected the
moment it appears. For comparison the same generator is also run with 16-, 24-
and 32-bit truncation, which shows how collisions appear as the tag gets
shorter - the birthday bound in practice.
"""

import hashlib
import math
import os
import random
import time

N_MESSAGES = 1_000_000
TRUNC_TESTS = [(16, 200), (24, 60), (32, 15)]     # (bits, number of trials)

_rng = random.Random(int.from_bytes(os.urandom(32), "big"))


def message(i: int) -> bytes:
    """Unique message: counter + 64 random bits. Uniqueness is what matters,
    the nonce only has to look random, not be cryptographically strong."""
    return f"LGU-IS-Lab06 | msg {i:07d} | nonce {_rng.getrandbits(64):016x}".encode()


def full_sha256_scan(n: int):
    """Hash n random messages, return (collisions, unique, elapsed)."""
    seen = {}
    collisions = []
    t0 = time.perf_counter()
    for i in range(n):
        msg = message(i)
        d = hashlib.sha256(msg).digest()
        if d in seen:
            collisions.append((seen[d], msg, d.hex()))
        else:
            seen[d] = msg
    return collisions, len(seen), time.perf_counter() - t0


def first_collision(bits: int, offset: int):
    """Return the number of messages needed for the first collision on a
    `bits`-bit tag, or None if the cap is reached."""
    nbytes = (bits + 7) // 8
    mask = (1 << bits) - 1
    seen = {}
    for i in range(4_000_000):
        msg = message(offset + i)
        d = hashlib.sha256(msg).digest()
        tag = int.from_bytes(d[:nbytes], "big") & mask
        if tag in seen:
            return i + 1
        seen[tag] = i
    return None


def main():
    bar = "=" * 68
    print(bar)
    print(" TASK 2 : SHA-256 COLLISION DETECTION (COMPLETE 256-BIT HASH)")
    print(bar)
    print("Hash function      : SHA-256, no truncation")
    print("Digest size        : 256 bits = 32 bytes")
    print(f"Messages to hash   : {N_MESSAGES:,}")
    print("Message format     : counter + 64 random bits (all distinct)")
    print()

    print("-- Scanning " + "-" * 55)
    collisions, unique, elapsed = full_sha256_scan(N_MESSAGES)

    print(f"Messages generated : {N_MESSAGES:,}")
    print(f"Unique digests     : {unique:,}")
    print(f"Collisions found   : {len(collisions)}")
    print(f"Elapsed            : {elapsed:.2f} s")
    print(f"Throughput         : {N_MESSAGES / elapsed:,.0f} hashes/s")
    print()
    print(f"Digest space       : 2^256 = {2.0 ** 256:.3e}")
    print(f"Birthday bound     : 2^128 = {2.0 ** 128:.3e} messages for 50% chance")
    p = N_MESSAGES * (N_MESSAGES - 1) / 2.0 ** 257
    print(f"P(collision) after : {p:.3e}   (n^2 / 2^257)")
    print(f"Years at 1e9/s     : {2.0 ** 128 / 1e9 / 31_536_000:.3e}")
    print()
    if not collisions:
        print("Result             : no collision found")
        print("Reason             : 2^128 work factor is beyond any machine")
        print("Conclusion         : complete SHA-256 behaves as collision resistant")
    print()

    # ---------------- truncation scaling ----------------
    print("-- Same generator, truncated tags " + "-" * 33)
    print(f"{'Bits':>5} {'Tag space':>14} {'Trials':>7} {'Mean msgs':>11} "
          f"{'Birthday bound':>15} {'Ratio':>7}")
    rows = []
    offset = 10_000_000
    for bits, trials in TRUNC_TESTS:
        counts = []
        for _ in range(trials):
            c = first_collision(bits, offset)
            offset += 5_000_000
            counts.append(c)
        mean = sum(counts) / len(counts)
        bound = math.sqrt(math.pi / 2 * (1 << bits))
        rows.append((bits, mean, bound))
        print(f"{bits:>5} {1 << bits:>14,} {trials:>7} {mean:>11,.0f} "
              f"{bound:>15,.0f} {mean / bound:>6.2f}x")
    print()
    print("Each 8 extra bits of tag multiply the work by about 2^4 = 16")
    for a, b in zip(rows, rows[1:]):
        print(f"{a[0]} -> {b[0]} bits : {b[1] / a[1]:.1f}x more messages "
              f"(theory 16.0x)")
    print()
    print("Extrapolation to the full digest")
    print(f"  32-bit tag  : {rows[-1][1]:,.0f} messages")
    print(f"  +224 bits   : 2^112 x more work -> 2^128 messages, unreachable")
    print(bar)


if __name__ == "__main__":
    main()
