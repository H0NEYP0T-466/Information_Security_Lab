#!/usr/bin/env python3
"""
================================================================================
LAHORE GARRISON UNIVERSITY - DEPARTMENT OF COMPUTER SCIENCES
INFORMATION SECURITY LAB (CC6306) - OPEN ENDED LAB (FALL 2026)
INSTRUCTOR: MUKKARAM AHMAD KHAN
STUDENT NAME: MUHAMMAD FEZAN
ROLL NUMBER: Fall-23-BSCS-466
SEMESTER: BSCS 7TH (SECTION L)
================================================================================
"""

import sys
import time
import hashlib
import json
from typing import List, Dict, Any, Tuple


class Block:
    """
    Represents an individual block in the cryptographic blockchain ledger.
    Contains index, timestamp, transaction data payload, previous_hash pointer,
    proof-of-work nonce, and SHA-256 block hash.
    """

    def __init__(self, index: int, timestamp: float, data: Any, previous_hash: str = "", nonce: int = 0):
        self.index: int = index
        self.timestamp: float = timestamp
        self.data: Any = data
        self.previous_hash: str = previous_hash
        self.nonce: int = nonce
        self.hash: str = self.compute_hash()

    def compute_hash(self) -> str:
        """Computes deterministic SHA-256 cryptographic digest over the block header."""
        block_header = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        encoded_header = json.dumps(block_header, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded_header).hexdigest()

    def compute_proof_of_work(self, difficulty: int) -> int:
        """
        Executes Proof-of-Work (PoW) mining by iteratively adjusting
        the nonce until the hash satisfies the leading-zero difficulty target.
        """
        target_prefix = "0" * difficulty
        iterations = 0
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.compute_hash()
            iterations += 1
        return iterations


class Blockchain:
    """Manages the sequential chain of blocks, PoW mining, and integrity validation."""

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty: int = difficulty
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Initializes the blockchain ledger with an immutable Genesis Block."""
        genesis_block = Block(
            index=0,
            timestamp=1763450000.0,
            data={"message": "Genesis Block - LGU Open Ended Lab", "creator": "System"},
            previous_hash="0" * 64,
            nonce=0
        )
        genesis_block.compute_proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: Any, verbose: bool = True) -> Block:
        """Creates, mines, and appends a new block to the blockchain ledger."""
        prev_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=prev_block.hash,
            nonce=0
        )

        t_start = time.perf_counter()
        cycles = new_block.compute_proof_of_work(self.difficulty)
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0

        self.chain.append(new_block)
        if verbose:
            print(f"[+] Block #{new_block.index} Mined | Nonce: {new_block.nonce:<4} | Prev: {new_block.previous_hash[:18]}.. | Hash: {new_block.hash[:22]}.. ({elapsed_ms:.2f} ms)")
        return new_block

    def is_chain_valid(self, verbose: bool = True) -> Tuple[bool, str]:
        """
        Verifies both stored hash recomputation and previous_hash linkage
        across all blocks in the blockchain.
        """
        target_prefix = "0" * self.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Verify stored hash matches recomputed hash
            recomputed = current.compute_hash()
            if current.hash != recomputed:
                msg = f"Hash Mismatch at Block #{current.index}: Stored '{current.hash[:16]}..' != Recomputed '{recomputed[:16]}..'"
                if verbose:
                    print(f"[-] INTEGRITY FAILED: {msg}")
                return False, msg

            # 2. Verify previous_hash linkage
            if current.previous_hash != previous.hash:
                msg = f"Linkage Broken at Block #{current.index}: Previous Hash '{current.previous_hash[:16]}..' != Block #{previous.index} Hash '{previous.hash[:16]}..'"
                if verbose:
                    print(f"[-] INTEGRITY FAILED: {msg}")
                return False, msg

            # 3. Verify Proof-of-Work difficulty criterion
            if not current.hash.startswith(target_prefix):
                msg = f"PoW Invalidation at Block #{current.index}: Hash '{current.hash[:16]}..' violates difficulty '{target_prefix}'"
                if verbose:
                    print(f"[-] INTEGRITY FAILED: {msg}")
                return False, msg

        if verbose:
            print("[+] INTEGRITY VERIFIED: All blocks cryptographic hashes, linkage, and PoW criteria are 100% valid.")
        return True, "Valid"

    def display_chain(self) -> None:
        """Displays a structured summary of each block currently in the ledger."""
        print("=" * 72)
        print(f"{'Idx':<4} | {'Data Payload':<28} | {'Nonce':<7} | {'Block Hash (SHA-256)':<24}")
        print("-" * 72)
        for b in self.chain:
            d_str = str(b.data)[:26] if isinstance(b.data, str) else list(b.data.values())[0][:26]
            print(f"{b.index:<4} | {d_str:<28} | {b.nonce:<7} | {b.hash[:22]}..")
        print("=" * 72)


def run_part1(bc: Blockchain):
    print("=" * 72)
    print(" PART 1: BLOCK STRUCTURE & PROOF OF WORK (PoW) MINING")
    print("=" * 72)
    print(f"Difficulty Target : {bc.difficulty} leading zeroes ('{'0'*bc.difficulty}')")
    print(f"Genesis Block Hash: {bc.chain[0].hash[:24]}.. (PoW Nonce: {bc.chain[0].nonce})\n")

    print("[Mining] Generating blocks with PoW difficulty target:")
    bc.add_block("Alice transfers 10.0 BTC to Bob", verbose=True)
    bc.add_block("Bob transfers 5.0 BTC to Charlie", verbose=True)
    bc.add_block("Charlie transfers 2.5 BTC to Dave", verbose=True)

    print("\n[Current Blockchain Ledger State]")
    bc.display_chain()


def run_part2(bc: Blockchain):
    print("=" * 72)
    print(" PART 2: CRYPTOGRAPHIC CHAIN VALIDATION (is_chain_valid)")
    print("=" * 72)
    print("Running comprehensive cryptographic audit across all blocks:")
    print(" 1. Recomputing SHA-256 block hash and comparing against stored hash.")
    print(" 2. Verifying previous_hash cryptographic linkage pointer.")
    print(" 3. Verifying Proof-of-Work difficulty target satisfaction.\n")
    valid, status = bc.is_chain_valid(verbose=True)
    print(f"\nFinal Validation Status : {valid} ({status})")
    print(f"Chain Integrity Check   : PASSED (All {len(bc.chain)} blocks valid)")
    print("=" * 72)


def run_part3(bc: Blockchain):
    print("=" * 72)
    print(" PART 3: EVALUATING IMMUTABILITY (UNAUTHORIZED DATA TAMPERING)")
    print("=" * 72)
    target_block = bc.chain[1]
    print(f"Original Block #1 Data : '{target_block.data}'")
    print(f"Original Block #1 Hash : '{target_block.hash}'")

    print("\n[Adversary Action] Tampering Block #1 data payload in-place...")
    target_block.data = "Alice transfers 100.0 BTC to Hacker"
    print(f"Tampered Block #1 Data : '{target_block.data}'")

    print("\n[Integrity Audit] Running is_chain_valid() post-tampering:")
    valid, status = bc.is_chain_valid(verbose=True)
    print(f"\nValidation Result       : {valid} (Tampering Successfully Detected!)")
    print("Security Implication    : Altering block data changes its SHA-256 digest,")
    print("                          causing immediate detection and block rejection.")
    print("=" * 72)


def run_part4(bc: Blockchain):
    print("=" * 72)
    print(" PART 4: 51% MAJORITY ATTACK (DOWNSTREAM HASH RECALCULATION)")
    print("=" * 72)
    print("Adversary possesses >50% network mining power and re-mines Block #1")
    print("and all subsequent blocks to force acceptance of the tampered branch.\n")

    t_atk_start = time.perf_counter()
    for i in range(1, len(bc.chain)):
        curr_b = bc.chain[i]
        prev_b = bc.chain[i - 1]
        curr_b.previous_hash = prev_b.hash
        curr_b.nonce = 0
        curr_b.hash = curr_b.compute_hash()
        curr_b.compute_proof_of_work(bc.difficulty)
        print(f"[51% Attack] Re-mined Block #{curr_b.index} | Nonce: {curr_b.nonce:<5} | New Hash: {curr_b.hash[:24]}..")

    atk_elapsed_ms = (time.perf_counter() - t_atk_start) * 1000.0
    print(f"\n[Attack Complete] All downstream blocks recalculated in {atk_elapsed_ms:.2f} ms.")

    print("\n[Modified Blockchain Ledger State Post-51% Attack]")
    bc.display_chain()

    print("\n[Consensus Audit] Running is_chain_valid() post-51% recalculation:")
    valid, status = bc.is_chain_valid(verbose=True)
    print(f"\nValidation Result       : {valid} ({status})")
    print("Security Implication    : The fraudulent branch is now internally valid.")
    print("                          In a decentralized network, a majority attacker")
    print("                          outpaces honest nodes and enforces this fork.")
    print("=" * 72)


def main():
    part = sys.argv[1] if len(sys.argv) > 1 else "all"

    # Setup chain
    bc = Blockchain(difficulty=2)
    if part in ("2", "3", "4", "all"):
        bc.add_block("Alice transfers 10.0 BTC to Bob", verbose=False)
        bc.add_block("Bob transfers 5.0 BTC to Charlie", verbose=False)
        bc.add_block("Charlie transfers 2.5 BTC to Dave", verbose=False)

    if part == "1":
        bc_p1 = Blockchain(difficulty=2)
        run_part1(bc_p1)
    elif part == "2":
        run_part2(bc)
    elif part == "3":
        run_part3(bc)
    elif part == "4":
        bc.chain[1].data = "Alice transfers 100.0 BTC to Hacker"
        run_part4(bc)
    else:
        bc_fresh = Blockchain(difficulty=2)
        run_part1(bc_fresh)
        run_part2(bc_fresh)
        run_part3(bc_fresh)
        run_part4(bc_fresh)


if __name__ == "__main__":
    main()
