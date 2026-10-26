#!/usr/bin/env python3
"""
Task 4 - Password Hashing with a Random Salt and Verification
Information Security Lab 06 (Secure Hash Functions)
Muhammad Fezan - Fall-23-BSCS-466

Two users with the same password must not produce the same stored hash,
otherwise one rainbow table cracks both accounts at once. A random salt per
user fixes that: the attacker has to rebuild the table for every single record.

Stored record = algorithm | iterations | salt | derived key
The plaintext password is never stored anywhere.
"""

import hashlib
import hmac
import os

ITERATIONS = 100_000
SALT_BYTES = 16
DKLEN = 32


def hash_password(password: str, salt: bytes = None, iterations: int = ITERATIONS) -> dict:
    """Return a self-describing record. Salt is random when not supplied."""
    if salt is None:
        salt = os.urandom(SALT_BYTES)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, DKLEN)
    return {
        "algorithm": "pbkdf2_hmac_sha256",
        "iterations": iterations,
        "salt": salt.hex(),
        "hash": dk.hex(),
    }


def verify_password(password: str, record: dict) -> bool:
    """Recompute with the stored salt/iterations and compare in constant time."""
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(record["salt"]),
        record["iterations"],
        len(bytes.fromhex(record["hash"])),
    )
    return hmac.compare_digest(dk, bytes.fromhex(record["hash"]))


def show_record(rec: dict, label: str = "Stored record"):
    print(f"{label}")
    print(f"  algorithm  : {rec['algorithm']}")
    print(f"  iterations : {rec['iterations']:,}")
    print(f"  salt       : {rec['salt']}   ({len(rec['salt']) // 2} bytes, random)")
    print(f"  hash       : {rec['hash']}")
    print(f"  record size: {len(rec['salt']) // 2 + len(rec['hash']) // 2} bytes "
          f"(salt + derived key)")


def main():
    bar = "=" * 68
    print(bar)
    print(" TASK 4 : PASSWORD HASHING WITH SALT + PBKDF2 VERIFICATION")
    print(bar)
    print(f"Algorithm          : PBKDF2-HMAC-SHA256")
    print(f"Iterations         : {ITERATIONS:,}")
    print(f"Salt               : {SALT_BYTES} random bytes per password")
    print(f"Derived key        : {DKLEN} bytes")
    print()

    # ---------------- registration ----------------
    print("-- Registration " + "-" * 52)
    pwd = input("Enter password to register : ")
    record = hash_password(pwd)
    print()
    show_record(record)
    print()
    print("Plaintext password stored : False")
    print()

    # ---------------- verification ----------------
    print("-- Verification " + "-" * 52)
    attempt = input("Enter password to verify   : ")
    ok = verify_password(attempt, record)
    print()
    print(f"Password accepted  : {ok}")
    print(f"Comparison         : hmac.compare_digest (constant time)")
    print()

    wrong = input("Enter a wrong password     : ")
    ok2 = verify_password(wrong, record)
    print()
    print(f"Password accepted  : {ok2}")
    print(f"Result             : {'access granted' if ok2 else 'access denied'}")
    print()

    # ---------------- salt uniqueness ----------------
    print("-- Salt uniqueness " + "-" * 49)
    same_a = hash_password("HashLab@2026")
    same_b = hash_password("HashLab@2026")
    print("User A (password = HashLab@2026)")
    print(f"  salt : {same_a['salt']}")
    print(f"  hash : {same_a['hash']}")
    print("User B (same password)")
    print(f"  salt : {same_b['salt']}")
    print(f"  hash : {same_b['hash']}")
    print()
    print(f"Same password, same salt  : {same_a['salt'] == same_b['salt']}")
    print(f"Same password, same hash  : {same_a['hash'] == same_b['hash']}")
    print(f"A verifies its password   : {verify_password('HashLab@2026', same_a)}")
    print(f"B verifies its password   : {verify_password('HashLab@2026', same_b)}")
    print(f"A's record rejects a wrong password : {not verify_password('other', same_a)}")
    print()

    # ---------------- rainbow table note ----------------
    print("-- Attack impact " + "-" * 51)
    print(f"Unsalted, 1M-entry rainbow table cracks every user with that password")
    print(f"With a {SALT_BYTES}-byte salt the attacker needs 2^{SALT_BYTES * 8} = "
          f"{2 ** (SALT_BYTES * 8):.3e} tables")
    print(f"Cost multiplier per user  : {2 ** (SALT_BYTES * 8):.3e}")
    print(f"Stored hash is useless for a second account: True")
    print(bar)


if __name__ == "__main__":
    main()
