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
PROBLEM:
    Implement a Blockchain Integrity & Consensus Prototype in Python using
    SHA-256 cryptographic hashing. Design Block and Blockchain classes
    incorporating Proof of Work (PoW) mining (compute_proof_of_work()),
    cryptographic chain validation (is_chain_valid()), unauthorized data
    tampering detection, and a 51% majority attack simulation.
================================================================================
"""

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
        """
        Computes the deterministic SHA-256 cryptographic digest over the block header.
        Uses sorted-key JSON serialization to guarantee consistency across execution runs.
        """
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
        Executes Proof-of-Work (PoW) mining.
        Iteratively adjusts the nonce until the resulting SHA-256 hash
        matches the required leading-zero difficulty target.
        """
        target_prefix = "0" * difficulty
        iterations = 0
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.compute_hash()
            iterations += 1
        return iterations


class Blockchain:
    """
    Manages the sequential chain of blocks, proof-of-work mining difficulty,
    cryptographic integrity verification, and attack simulations.
    """

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty: int = difficulty
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Initializes the blockchain ledger with an immutable Genesis Block."""
        genesis_block = Block(
            index=0,
            timestamp=1763450000.0,
            data={"message": "Genesis Block - LGU Open Ended Lab (Fall 2026)", "creator": "System"},
            previous_hash="0" * 64,
            nonce=0
        )
        genesis_block.compute_proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Returns the most recent block in the active chain."""
        return self.chain[-1]

    def add_block(self, data: Any) -> Block:
        """
        Creates, mines, and appends a new block to the blockchain ledger.
        """
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
        print(f"[+] Block #{new_block.index} successfully mined!")
        print(f"    Data Payload  : {new_block.data}")
        print(f"    Nonce (PoW)   : {new_block.nonce} ({cycles} iterations in {elapsed_ms:.2f} ms)")
        print(f"    Previous Hash : {new_block.previous_hash}")
        print(f"    Block Hash    : {new_block.hash}\n")
        return new_block

    def is_chain_valid(self, verbose: bool = True) -> Tuple[bool, str]:
        """
        Verifies both stored hash recomputation and previous_hash linkage
        across all blocks in the blockchain.
        Returns (True, 'Valid') or (False, Error_Reason).
        """
        target_prefix = "0" * self.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Verify block stored hash matches recomputed hash
            recomputed = current.compute_hash()
            if current.hash != recomputed:
                msg = f"Hash Mismatch at Block #{current.index}: Stored '{current.hash[:16]}..' != Recomputed '{recomputed[:16]}..'"
                if verbose:
                    print(f"[-] INTEGRITY FAILED: {msg}")
                return False, msg

            # 2. Verify previous_hash linkage matches predecessor's actual hash
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


def main():
    print("=" * 72)
    print(" LAHORE GARRISON UNIVERSITY - OPEN ENDED LAB (OEL)")
    print(" INFORMATION SECURITY LAB (CC6306) - FALL 2026")
    print(" Student: Muhammad Fezan (Fall-23-BSCS-466) | Instructor: Mukkaram Ahmad Khan")
    print("=" * 72)

    # --------------------------------------------------------------------------
    # QUESTION 1 & 2: BLOCK CREATION, POW MINING & CHAIN VALIDATION
    # --------------------------------------------------------------------------
    print("\n[PART 1] INITIALIZING BLOCKCHAIN & MINING BLOCKS (PoW Difficulty = 2)")
    print("-" * 72)
    blockchain = Blockchain(difficulty=2)
    print(f"Genesis Block initialized. Hash: {blockchain.chain[0].hash}\n")

    print("[Mining] Adding Block #1...")
    blockchain.add_block("Alice transfers 10.0 BTC to Bob")

    print("[Mining] Adding Block #2...")
    blockchain.add_block("Bob transfers 5.0 BTC to Charlie")

    print("[Mining] Adding Block #3...")
    blockchain.add_block("Charlie transfers 2.5 BTC to Dave")

    print("\n[Current Blockchain Ledger State]")
    blockchain.display_chain()

    print("\n[PART 2] RUNNING INITIAL CHAIN VALIDATION (is_chain_valid)")
    print("-" * 72)
    valid, status = blockchain.is_chain_valid(verbose=True)
    print(f"Validation Result: {valid} ({status})")

    # --------------------------------------------------------------------------
    # QUESTION 3: UNAUTHORIZED DATA TAMPERING SIMULATION
    # --------------------------------------------------------------------------
    print("\n[PART 3] EVALUATING IMMUTABILITY: UNAUTHORIZED DATA TAMPERING")
    print("-" * 72)
    target_block = blockchain.chain[1]
    print(f"Original Block #1 Data: '{target_block.data}'")
    print(f"Original Block #1 Hash: '{target_block.hash}'")

    # Adversary alters transaction data in-place
    print("\n[Adversary Action] Tampering Block #1 data payload...")
    target_block.data = "Alice transfers 100.0 BTC to Hacker"
    print(f"Tampered Block #1 Data: '{target_block.data}'")

    print("\n[Integrity Audit] Running is_chain_valid() post-tampering:")
    valid_post_tamper, status_post_tamper = blockchain.is_chain_valid(verbose=True)
    print(f"Validation Result: {valid_post_tamper} (Tampering Successfully Detected!)")

    # --------------------------------------------------------------------------
    # QUESTION 4: 51% MAJORITY ATTACK SIMULATION (DOWNSTREAM RECALCULATION)
    # --------------------------------------------------------------------------
    print("\n[PART 4] SIMULATING 51% MAJORITY ATTACK (DOWNSTREAM HASH RECALCULATION)")
    print("-" * 72)
    print("Adversary possesses >50% network mining power and re-mines Block #1")
    print("and all subsequent blocks to bypass cryptographic validation.\n")

    t_atk_start = time.perf_counter()
    for i in range(1, len(blockchain.chain)):
        curr_b = blockchain.chain[i]
        prev_b = blockchain.chain[i - 1]

        # 1. Update linkage to modified predecessor
        curr_b.previous_hash = prev_b.hash
        curr_b.nonce = 0
        curr_b.hash = curr_b.compute_hash()

        # 2. Re-mine Proof-of-Work to satisfy target difficulty
        remined_cycles = curr_b.compute_proof_of_work(blockchain.difficulty)
        print(f"[51% Attack] Re-mined Block #{curr_b.index} | Nonce: {curr_b.nonce} | New Hash: {curr_b.hash[:22]}..")

    atk_elapsed_ms = (time.perf_counter() - t_atk_start) * 1000.0
    print(f"\n[Attack Complete] All downstream blocks recalculated in {atk_elapsed_ms:.2f} ms.")

    print("\n[Modified Blockchain Ledger State Post-51% Attack]")
    blockchain.display_chain()

    print("\n[Consensus Audit] Running is_chain_valid() post-51% recalculation:")
    valid_post_attack, status_post_attack = blockchain.is_chain_valid(verbose=True)
    print(f"Validation Result: {valid_post_attack} ({status_post_attack})")
    print("Security Implication: The fraudulent branch is now internally cryptographically valid.")
    print("In a decentralized P2P network, an attacker with >50% hash power can outpace honest")
    print("miners, forcing peers to adopt the tampered ledger via Nakamoto Consensus.")
    print("=" * 72)


if __name__ == "__main__":
    main()
