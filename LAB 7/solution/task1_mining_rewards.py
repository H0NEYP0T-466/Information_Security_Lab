#!/usr/bin/env python3
"""
Information Security Lab - Week 07
Task 1: Simplified Blockchain Mining Reward System
Author: Muhammad Fezan (Fall-23-BSCS-466)
Course: Information Security Lab (7th Semester - Fall 2026)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Lahore Garrison University - Department of Computer Science
"""

import time
import hashlib
import json
from typing import List, Dict, Any


class Block:
    """Represents a single block in the blockchain ledger."""

    def __init__(self, index: int, timestamp: float, data: Dict[str, Any],
                 previous_hash: str = "", nonce: int = 0):
        self.index: int = index
        self.timestamp: float = timestamp
        self.data: Dict[str, Any] = data
        self.previous_hash: str = previous_hash
        self.nonce: int = nonce
        self.hash: str = self.compute_hash()

    def compute_hash(self) -> str:
        """Calculates deterministic SHA-256 digest over the block payload."""
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def proof_of_work(self, difficulty: int) -> None:
        """Finds a nonce producing a hash with required leading zeros."""
        target_prefix = "0" * difficulty
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.compute_hash()


class Blockchain:
    """Maintains blockchain ledger, mining difficulty, and miner balances."""

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty: int = difficulty
        self.mining_reward: float = 50.0  # Requirement: 50 coins reward per block
        self.wallets: Dict[str, float] = {}
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Initializes the blockchain with an immutable Genesis Block."""
        genesis_block = Block(
            index=0,
            timestamp=1763450000.0,
            data={"type": "Genesis", "miner": "SYSTEM", "reward": 0.0},
            previous_hash="0" * 64,
            nonce=0
        )
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mine_block(self, miner_address: str) -> Block:
        """
        Mines a new block for the given miner_address.
        Adds reward information to the block, performs proof-of-work,
        appends the block to the chain, and adds 50 coins to the miner's wallet.
        """
        prev_block = self.get_latest_block()
        new_index = prev_block.index + 1

        reward_data = {
            "type": "Mining_Reward",
            "miner": miner_address,
            "reward": self.mining_reward,
            "note": f"Block #{new_index} coinbase"
        }

        new_block = Block(
            index=new_index,
            timestamp=time.time(),
            data=reward_data,
            previous_hash=prev_block.hash,
            nonce=0
        )

        t_start = time.perf_counter()
        new_block.proof_of_work(self.difficulty)
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0

        self.chain.append(new_block)

        if miner_address not in self.wallets:
            self.wallets[miner_address] = 0.0
        self.wallets[miner_address] += self.mining_reward

        print(f"[+] Block #{new_index} mined by {miner_address} | Nonce: {new_block.nonce} ({elapsed_ms:.2f} ms)")
        print(f"    Hash: {new_block.hash} | Reward: +{self.mining_reward} coins")
        return new_block

    def is_chain_valid(self) -> bool:
        """Verifies cryptographic link and hash integrity of all blocks."""
        target_prefix = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.compute_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
            if not curr.hash.startswith(target_prefix):
                return False
        return True

    def print_rewards(self) -> None:
        """Displays miner addresses and their total earned rewards."""
        print("=" * 68)
        print("           MINER REWARD BALANCES & WALLET LEDGER")
        print("=" * 68)
        print(f"{'Miner Address':<34} | {'Blocks':<8} | {'Total Reward (Coins)':<20}")
        print("-" * 68)
        for miner, balance in sorted(self.wallets.items()):
            blocks = int(balance // self.mining_reward)
            print(f"{miner:<34} | {blocks:<8} | {balance:>14.2f} coins")
        print("-" * 68)
        print(f"Total Active Miners: {len(self.wallets)} | Total Currency Mined: {sum(self.wallets.values()):.2f} coins")
        print("=" * 68)

    def display_chain_summary(self) -> None:
        """Displays a compact summary table of the entire blockchain."""
        print("\n" + "=" * 68)
        print(f"{'Idx':<4} | {'Miner / Type':<26} | {'Nonce':<7} | {'Block Hash (Prefix)':<22}")
        print("-" * 68)
        for b in self.chain:
            m = b.data.get("miner", b.data.get("type", "Block"))
            print(f"{b.index:<4} | {m:<26} | {b.nonce:<7} | {b.hash[:20]}..")
        print("=" * 68)


def main():
    print("=" * 68)
    print(" TASK 1: SIMPLIFIED BLOCKCHAIN MINING REWARD SYSTEM")
    print(" Author: Muhammad Fezan (Fall-23-BSCS-466) | Course: IS(L)")
    print("=" * 68)

    print("\n[Step 1] Initializing Blockchain with Genesis Block...")
    blockchain = Blockchain(difficulty=2)
    print(f"         Mining Reward : {blockchain.mining_reward} coins")
    print(f"         PoW Difficulty: {blockchain.difficulty} leading zeros")
    print(f"         Genesis Hash  : {blockchain.chain[0].hash}\n")

    print("[Step 2] Mining blocks for multiple miners (Alice, Bob, Fezan)...")
    blockchain.mine_block("0x71A4_Alice_Miner")
    blockchain.mine_block("0x94B2_Bob_Miner")
    blockchain.mine_block("0x71A4_Alice_Miner")
    blockchain.mine_block("0x466F_Fezan_Miner")

    print("\n[Step 3] Displaying miner rewards:")
    blockchain.print_rewards()

    print("\n[Step 4] Cryptographic chain validation:")
    print(f"         Total blocks in chain : {len(blockchain.chain)}")
    print(f"         Chain integrity valid : {blockchain.is_chain_valid()}")

    print("\n[Step 5] Final Blockchain Ledger Summary:")
    blockchain.display_chain_summary()


if __name__ == "__main__":
    main()
