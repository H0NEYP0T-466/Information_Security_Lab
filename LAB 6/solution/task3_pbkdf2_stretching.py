#!/usr/bin/env python3
"""
Task 3 - Hash Stretching with PBKDF2-HMAC-SHA256
Information Security Lab 06 (Secure Hash Functions)
Muhammad Fezan - Fall-23-BSCS-466

A single SHA-256 of a password takes about one microsecond, so an attacker can
test billions of candidates per second. PBKDF2 slows the attacker down by
re-hashing the result a large number of times. The cost of one legitimate login
becomes the cost of one guess for the attacker.

This program derives the same key with 1,000 / 10,000 / 100,000 iterations and
measures how the time grows.
"""

import hashlib

import statistics
import time

PASSWORD = "HashLab@2026"
SALT = bytes.fromhex("4c47552d49534c414230362d53414c54")   # fixed 16-byte salt
ITERATIONS = [1_000, 10_000, 100_000]
REPEATS = 10
DKLEN = 32                                                  # 256-bit derived key
GPU_HASHES_PER_SEC = 1e10                                   # one high-end GPU
CANDIDATES = 36 ** 6                                        # a-z0-9, 6 chars


def derive(password: str, salt: bytes, iterations: int, dklen: int = DKLEN) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen)


def timed(password: str, salt: bytes, iterations: int):
    """Run REPEATS derivations, return (best_ms, mean_ms, derived_key)."""
    samples, dk = [], None
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        dk = derive(password, salt, iterations)
        samples.append((time.perf_counter() - t0) * 1000)
    return min(samples), statistics.mean(samples), dk


def human(seconds: float) -> str:
    if seconds < 1e-3:
        return f"{seconds * 1e6:.2f} us"
    if seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    if seconds < 60:
        return f"{seconds:.1f} s"
    if seconds < 3600:
        return f"{seconds / 60:.1f} min"
    if seconds < 86400:
        return f"{seconds / 3600:.2f} h"
    return f"{seconds / 86400:.2f} days"


def main():
    bar = "=" * 68
    print(bar)
    print(" TASK 3 : HASH STRETCHING - PBKDF2-HMAC-SHA256")
    print(bar)
    print("Password           : " + PASSWORD + f"  ({len(PASSWORD)} chars)")
    print(f"Salt (fixed)       : {SALT.hex()}")
    print(f"Derived key length : {DKLEN} bytes (256 bits)")
    print(f"Repeats per timing : {REPEATS} (fastest run reported)")
    print()

    print("-- Iteration cost " + "-" * 49)
    print(f"{'Iterations':>12} {'Best (ms)':>11} {'Mean (ms)':>11} "
          f"{'us / iter':>11} {'Cost vs 1k':>11}")
    results = []
    base_ms = None
    for it in ITERATIONS:
        best, mean, dk = timed(PASSWORD, SALT, it)
        if base_ms is None:
            base_ms = best
        results.append((it, best, mean, dk))
        print(f"{it:>12,} {best:>11.2f} {mean:>11.2f} {best / it * 1000:>11.2f} "
              f"{best / base_ms:>10.1f}x")
    print()
    us = [best / it * 1000 for it, best, _, _ in results]
    print(f"Per-iteration cost stays in a narrow band ({min(us):.2f} - {max(us):.2f} us)")
    print("while the iteration count changes 100x, so the total time is linear in")
    print("the iteration count: 10x iterations -> ~10x slower.")
    print()

    print("-- Derived keys " + "-" * 51)
    for it, _, _, dk in results:
        print(f"{it:>8,} iterations : {dk.hex()}")
    print()
    print(f"Keys differ with iteration count : "
          f"{len({dk for _, _, _, dk in results}) == len(results)}")
    print(f"Same parameters give same key    : "
          f"{derive(PASSWORD, SALT, 10_000) == derive(PASSWORD, SALT, 10_000)}")
    other = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    print(f"Different salt gives other key   : "
          f"{derive(PASSWORD, SALT, 10_000) != derive(PASSWORD, other, 10_000)}")
    print()

    # ---------------- attacker view ----------------
    print("-- Attacker view " + "-" * 51)
    print(f"GPU model          : {GPU_HASHES_PER_SEC:.0e} SHA-256 ops/s")
    print(f"Password space     : 36^6 = {CANDIDATES:,.0f} (6 chars, a-z0-9)")
    print()
    print(f"{'Iterations':>12} {'Guesses/s (GPU)':>17} {'1 guess':>10} "
          f"{'Exhaust space':>15}")
    for it, best, _, _ in results:
        gps = GPU_HASHES_PER_SEC / it
        print(f"{it:>12,} {gps:>17,.0f} {human(1 / gps):>10} "
              f"{human(CANDIDATES / gps):>15}")
    print()
    single = 1e10
    print(f"Unstretched SHA-256: {single:,.0f} guesses/s -> "
          f"{human(CANDIDATES / single)} to exhaust the space")
    it100k = results[-1][0]
    print(f"PBKDF2 100,000     : {single / it100k:,.0f} guesses/s -> "
          f"slowdown of {it100k:,}x")
    print()
    print(f"Measured cost of one login at 100,000 iterations: "
          f"{results[-1][1]:.1f} ms")
    print(bar)


if __name__ == "__main__":
    main()
