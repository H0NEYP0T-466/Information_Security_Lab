#!/usr/bin/env python3
"""
Information Security Lab - Week 07
Task 1: Simplified Blockchain Mining Reward System
Author: Muhammad Fezan (Fall-23-BSCS-466)
Course: Information Security Lab (7th Semester - Fall 2026)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Lahore Garrison University - Department of Computer Science

Objective:
    Simulate a proof-of-work blockchain that incentives miners by awarding
    a fixed mining reward (50 coins) per block and maintaining wallet balances.
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
        """
        Calculates SHA-256 digest over the block's header and payload.
        Ensures strict deterministic JSON serialization for repeatability.
        """
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
        """
        Mines the block by finding a nonce that yields a SHA-256 hash
        starting with a required number of leading zeroes.
        """
        target_prefix = "0" * difficulty
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.compute_hash()


class Blockchain:
    """
    Maintains the decentralized chain of blocks, ledger integrity,
    mining incentives, and individual miner wallet balances.
    """

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty: int = difficulty
        self.mining_reward: float = 50.0  # Fixed 50 coins reward per mined block
        self.wallets: Dict[str, float] = {}  # Tracks miner address -> balance
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Initializes the blockchain with an immutable Genesis Block."""
        genesis_data = {
            "type": "Genesis",
            "message": "Genesis Block - LGU Information Security Lab 07",
            "reward": 0.0,
            "miner": "SYSTEM_NETWORK"
        }
        genesis_block = Block(
            index=0,
            timestamp=1763450000.0,  # Fixed epoch timestamp for deterministic genesis
            data=genesis_data,
            previous_hash="0" * 64,
            nonce=0
        )
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Returns the most recently appended block in the chain."""
        return self.chain[-1]

    def mine_block(self, miner_address: str) -> Block:
        """
        Mines a new block awarded to the miner's address.
        Records the reward inside the block's data payload, verifies proof-of-work,
        appends the block to the ledger, and credits the miner's wallet.
        """
        prev_block = self.get_latest_block()
        new_index = prev_block.index + 1
        current_time = time.time()

        reward_data = {
            "type": "Mining_Reward",
            "miner": miner_address,
            "reward": self.mining_reward,
            "block_reward_note": f"Block #{new_index} coinbase transaction"
        }

        new_block = Block(
            index=new_index,
            timestamp=current_time,
            data=reward_data,
            previous_hash=prev_block.hash,
            nonce=0
        )

        # Execute Proof-of-Work mining
        t_start = time.perf_counter()
        new_block.proof_of_work(self.difficulty)
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0

        # Append to blockchain
        self.chain.append(new_block)

        # Credit miner's wallet with mining reward
        if miner_address not in self.wallets:
            self.wallets[miner_address] = 0.0
        self.wallets[miner_address] += self.mining_reward

        print(f"[+] Block #{new_index} successfully mined by {miner_address}!")
        print(f"    Hash      : {new_block.hash}")
        print(f"    Prev Hash : {new_block.previous_hash}")
        print(f"    Nonce     : {new_block.nonce} (solved in {elapsed_ms:.2f} ms)")
        print(f"    Reward    : +{self.mining_reward:.1f} coins credited\n")

        return new_block

    def is_chain_valid(self) -> bool:
        """Verifies the cryptographic link and hash integrity of all blocks."""
        target_prefix = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Verify current block's hash recomputation
            if curr.hash != curr.compute_hash():
                return False
            # Verify chain linkage
            if curr.previous_hash != prev.hash:
                return False
            # Verify proof of work difficulty
            if not curr.hash.startswith(target_prefix):
                return False
        return True

    def print_rewards(self) -> None:
        """Displays formatted ledger summary of all miner wallet addresses and balances."""
        print("=" * 68)
        print("           MINER REWARD BALANCES & WALLET LEDGER")
        print("=" * 68)
        print(f"{'Miner Address':<36} | {'Blocks Mined':<14} | {'Total Reward (Coins)':<18}")
        print("-" * 68)

        total_distributed = 0.0
        for miner, balance in sorted(self.wallets.items()):
            blocks_mined = int(balance // self.mining_reward)
            total_distributed += balance
            print(f"{miner:<36} | {blocks_mined:<14} | {balance:>12.2f} coins")

        print("-" * 68)
        print(f"Total Active Miners      : {len(self.wallets)}")
        print(f"Total Rewards Distributed: {total_distributed:.2f} coins")
        print("=" * 68)

    def display_chain(self) -> None:
        """Prints detailed overview of each block residing in the blockchain."""
        print("\n" + "=" * 68)
        print("                 CURRENT BLOCKCHAIN LEDGER")
        print("=" * 68)
        for blk in self.chain:
            print(f"Block Index  : {blk.index}")
            print(f"Timestamp    : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(blk.timestamp))}")
            print(f"Block Type   : {blk.data.get('type')}")
            print(f"Beneficiary  : {blk.data.get('miner')}")
            print(f"Reward Amount: {blk.data.get('reward')} coins")
            print(f"Nonce (PoW)  : {blk.nonce}")
            print(f"Prev Hash    : {blk.previous_hash}")
            print(f"Current Hash : {blk.hash}")
            print("-" * 68)


def main():
    print("=" * 68)
    print(" TASK 1: SIMPLIFIED BLOCKCHAIN MINING REWARD SYSTEM")
    print(" Author: Muhammad Fezan (Fall-23-BSCS-466) | Course: IS(L)")
    print("=" * 68)

    # 1. Instantiate Blockchain (Genesis block initialized, reward = 50 coins)
    print("\n[Step 1] Initializing Blockchain with Genesis Block...")
    blockchain = Blockchain(difficulty=2)
    print(f"         Reward per block : {blockchain.mining_reward} coins")
    print(f"         PoW Difficulty   : {blockchain.difficulty} leading zeroes")
    print(f"         Genesis Hash     : {blockchain.chain[0].hash}\n")

    # 2. Mine blocks for at least two different miners
    miner_alice = "0x71A4_Alice_Miner"
    miner_bob = "0x94B2_Bob_Miner"
    miner_fezan = "0x466F_Fezan_Miner"

    print("[Step 2] Mining blocks for multiple independent miners...")
    print(f"--- Mining Block 1 by {miner_alice} ---")
    blockchain.mine_block(miner_alice)

    print(f"--- Mining Block 2 by {miner_bob} ---")
    blockchain.mine_block(miner_bob)

    print(f"--- Mining Block 3 by {miner_alice} ---")
    blockchain.mine_block(miner_alice)

    print(f"--- Mining Block 4 by {miner_fezan} ---")
    blockchain.mine_block(miner_fezan)

    # 3. Print the rewards of all miners
    print("[Step 3] Displaying accumulated miner wallet rewards:")
    blockchain.print_rewards()

    # 4. Display the complete chain and verify cryptographic validity
    print("\n[Step 4] Cryptographic chain validation:")
    is_valid = blockchain.is_chain_valid()
    print(f"         Total blocks in chain : {len(blockchain.chain)}")
    print(f"         Chain integrity valid : {is_valid}")

    # 5. Display complete chain structure
    blockchain.display_chain()


if __name__ == "__main__":
    main()
