#!/usr/bin/env python3
"""
================================================================================
LAHORE GARRISON UNIVERSITY - DEPARTMENT OF COMPUTER SCIENCE
COURSE: INFORMATION SECURITY LAB (FALL 2026) - 7TH SEMESTER
INSTRUCTOR: SIR MUKKARAM AHMAD (ASST. LECT.)
STUDENT NAME: MUHAMMAD FEZAN
ROLL NUMBER: Fall-23-BSCS-466
SUBMISSION FILE: Fall-23-BSCS-466_Blockchain_HomeTask6-7.py
WEEK: 07 - BLOCKCHAIN TECHNOLOGY
================================================================================

TOPICS COVERED:
1. Simplified Blockchain Mining Reward System:
   - Blockchain class with Genesis block initialization.
   - Proof-of-Work mining with cryptographic SHA-256 block hashing.
   - Fixed 50-coin mining incentive per newly minted block.
   - Miner wallet tracking and reward distribution display.

2. Basic Blockchain Peer-to-Peer (P2P) Network Simulation:
   - Autonomous Node architecture maintaining isolated ledger copies.
   - Multi-node mesh (Node1, Node2, Node3).
   - Nakamoto Consensus (Longest Chain Rule) peer synchronization.
   - Distributed block propagation and network-wide convergence verification.
================================================================================
"""

import copy
import hashlib
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional


# ==============================================================================
# CORE BLOCKCHAIN PRIMITIVES
# ==============================================================================

class Block:
    """
    Represents an immutable, timestamped block in the cryptographic ledger.
    Contains metadata header and transaction/reward payload chained via SHA-256.
    """

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
        Computes the cryptographic SHA-256 digest across the block header.
        Uses sorted-key JSON serialization to guarantee deterministic digests.
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
        Finds a proof-of-work nonce producing a hash with required leading zeros.
        """
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()


class Blockchain:
    """
    Manages the sequential chain of blocks, ledger validation, mining difficulty,
    and miner wallet balances.
    """

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty: int = difficulty
        self.mining_reward: float = 50.0  # Requirement: 50 coins mining reward
        self.wallets: Dict[str, float] = {}  # Tracks miner addresses -> balance
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Initializes the blockchain with an immutable Genesis Block."""
        genesis_block = Block(
            index=0,
            timestamp=1763450000.0,
            data={"type": "Genesis", "message": "Genesis Block - LGU Blockchain"},
            previous_hash="0" * 64,
            nonce=0
        )
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Returns the most recently mined block in the chain."""
        return self.chain[-1]

    def mine_block(self, miner_address: str) -> Block:
        """
        Mines a new block awarded to the miner_address.
        Appends reward info to block data, performs Proof-of-Work, appends
        to the chain, and adds 50 coins to the miner's wallet balance.
        """
        prev_block = self.get_latest_block()
        new_index = prev_block.index + 1

        reward_data = {
            "type": "Mining_Reward",
            "miner": miner_address,
            "reward": self.mining_reward,
            "note": f"Block #{new_index} coinbase transaction"
        }

        new_block = Block(
            index=new_index,
            timestamp=time.time(),
            data=reward_data,
            previous_hash=prev_block.hash,
            nonce=0
        )

        t0 = time.perf_counter()
        new_block.proof_of_work(self.difficulty)
        dt = (time.perf_counter() - t0) * 1000.0

        # Append to chain
        self.chain.append(new_block)

        # Update miner's wallet
        if miner_address not in self.wallets:
            self.wallets[miner_address] = 0.0
        self.wallets[miner_address] += self.mining_reward

        print(f"[+] Block #{new_index} mined by {miner_address}!")
        print(f"    Hash      : {new_block.hash}")
        print(f"    Prev Hash : {new_block.previous_hash}")
        print(f"    Nonce     : {new_block.nonce} ({dt:.2f} ms)")
        print(f"    Reward    : +{self.mining_reward:.1f} coins added to wallet\n")
        return new_block

    def is_chain_valid(self, chain_to_check: Optional[List[Block]] = None) -> bool:
        """Validates cryptographic integrity and hash linkage."""
        c = chain_to_check if chain_to_check is not None else self.chain
        target = "0" * self.difficulty
        for i in range(1, len(c)):
            curr = c[i]
            prev = c[i - 1]
            if curr.hash != curr.compute_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
            if not curr.hash.startswith(target):
                return False
        return True

    def print_rewards(self) -> None:
        """Displays miner addresses and their total earned rewards."""
        print("=" * 68)
        print("             MINER REWARDS AND WALLET BALANCES")
        print("=" * 68)
        print(f"{'Miner Address':<36} | {'Blocks Mined':<14} | {'Total Reward':<14}")
        print("-" * 68)
        for miner, balance in sorted(self.wallets.items()):
            blocks = int(balance // self.mining_reward)
            print(f"{miner:<36} | {blocks:<14} | {balance:>8.2f} coins")
        print("-" * 68)
        print(f"Total Distributed: {sum(self.wallets.values()):.2f} coins across {len(self.wallets)} miners")
        print("=" * 68)


# ==============================================================================
# PEER-TO-PEER (P2P) NETWORK NODE
# ==============================================================================

class Node:
    """
    Simulates an independent peer node holding a local blockchain instance.
    """

    def __init__(self, node_name: str, difficulty: int = 2):
        self.node_name: str = node_name
        self.blockchain: Blockchain = Blockchain(difficulty=difficulty)

    def sync_with_node(self, peer: "Node") -> bool:
        """
        Synchronizes local blockchain ledger with a peer node.
        Applies Longest Chain Rule (Nakamoto Consensus) with verification.
        """
        peer_chain = peer.blockchain.chain
        print(f"[*] [{self.node_name}] Synchronizing with [{peer.node_name}]...")
        print(f"    Local blocks: {len(self.blockchain.chain)} | Peer blocks: {len(peer_chain)}")

        if not self.blockchain.is_chain_valid(peer_chain):
            print(f"    [-] Rejected: Peer [{peer.node_name}] has invalid blockchain.")
            return False

        if len(peer_chain) > len(self.blockchain.chain):
            old_len = len(self.blockchain.chain)
            self.blockchain.chain = copy.deepcopy(peer_chain)
            self.blockchain.wallets = copy.deepcopy(peer.blockchain.wallets)
            print(f"    [+] SUCCESS: [{self.node_name}] adopted longer chain from [{peer.node_name}]!")
            print(f"        Chain updated: {old_len} -> {len(self.blockchain.chain)} blocks.")
            return True
        else:
            print(f"    [=] No update required: Local chain is equal or longer.")
            return False

    def display_node_chain(self) -> None:
        """Displays summary of this node's ledger."""
        print(f"+{'-'*66}+")
        print(f"| Node: {self.node_name:<20} | Length: {len(self.blockchain.chain):<6} | Valid: {str(self.blockchain.is_chain_valid()):<6} |")
        print(f"+{'-'*66}+")
        for b in self.blockchain.chain:
            m = b.data.get("miner", b.data.get("type", "Block"))
            print(f"| Block #{b.index:<3} | Miner: {m:<22} | Hash: {b.hash[:18]}... |")
        print(f"+{'-'*66}+\n")


# ==============================================================================
# EXECUTION ROUTINES FOR TASK 1 AND TASK 2
# ==============================================================================

def run_task1():
    print("\n" + "#" * 70)
    print(" TASK 1: SIMPLIFIED BLOCKCHAIN MINING REWARD SYSTEM")
    print("#" * 70)

    # 1. Initialize Blockchain
    bc = Blockchain(difficulty=2)
    print(f"[Init] Blockchain created with Genesis Block.")
    print(f"       Mining Reward: {bc.mining_reward} coins")
    print(f"       Genesis Hash : {bc.chain[0].hash}\n")

    # 2. Mine blocks for at least two different miners
    miner_alice = "0x71A4_Alice_Miner"
    miner_bob = "0x94B2_Bob_Miner"

    print("[Mining] Generating blocks for multiple miners...")
    bc.mine_block(miner_alice)
    bc.mine_block(miner_bob)
    bc.mine_block(miner_alice)

    # 3. Print rewards
    print("[Ledger] Displaying miner rewards:")
    bc.print_rewards()

    # 4. Chain verification
    print(f"\n[Verification] Total Blocks: {len(bc.chain)} | Cryptographic Validity: {bc.is_chain_valid()}")


def run_task2():
    print("\n" + "#" * 70)
    print(" TASK 2: BASIC BLOCKCHAIN PEER-TO-PEER (P2P) NETWORK SIMULATION")
    print("#" * 70)

    # 1. Create three nodes
    print("[Setup] Initializing Node1, Node2, and Node3...")
    node1 = Node("Node1")
    node2 = Node("Node2")
    node3 = Node("Node3")

    # 2. Mine new block on Node1
    print("\n[Mining] Mining Block #1 on Node1...")
    node1.blockchain.mine_block("0xNode1_Miner")

    print("-- Network status before sync --")
    print(f"Node1 blocks: {len(node1.blockchain.chain)}")
    print(f"Node2 blocks: {len(node2.blockchain.chain)}")
    print(f"Node3 blocks: {len(node3.blockchain.chain)}")

    # 3. Synchronize Node2 and Node3 with Node1
    print("\n[Sync] Synchronizing Node2 and Node3 with Node1...")
    node2.sync_with_node(node1)
    node3.sync_with_node(node1)

    # 4. Display blockchain of each node
    print("\n[Display] Displaying blockchain state for all nodes post-sync:")
    node1.display_node_chain()
    node2.display_node_chain()
    node3.display_node_chain()

    # 5. Verify all nodes contain the same number of blocks
    print("[Verification] Verifying block counts and state consistency:")
    len1 = len(node1.blockchain.chain)
    len2 = len(node2.blockchain.chain)
    len3 = len(node3.blockchain.chain)
    same_count = (len1 == len2 == len3)
    same_hash = (node1.blockchain.get_latest_block().hash ==
                 node2.blockchain.get_latest_block().hash ==
                 node3.blockchain.get_latest_block().hash)

    print(f"Node1 length : {len1} | Latest Hash: {node1.blockchain.get_latest_block().hash}")
    print(f"Node2 length : {len2} | Latest Hash: {node2.blockchain.get_latest_block().hash}")
    print(f"Node3 length : {len3} | Latest Hash: {node3.blockchain.get_latest_block().hash}")
    print(f"Equal Length : {same_count}")
    print(f"Identical Tip: {same_hash}")
    print(f"Network P2P Convergence Status: {'SUCCESS' if (same_count and same_hash) else 'FAIL'}")


def main():
    print("=" * 70)
    print(" LAHORE GARRISON UNIVERSITY - DEPARTMENT OF COMPUTER SCIENCE")
    print(" INFORMATION SECURITY LAB - WEEK 07 HOME TASK SUBMISSION")
    print(" Student: Muhammad Fezan | Roll No: Fall-23-BSCS-466")
    print("=" * 70)
    run_task1()
    run_task2()
    print("\n" + "=" * 70)
    print(" ALL WEEK 07 TASKS COMPLETED SUCCESSFULLY.")
    print("=" * 70)


if __name__ == "__main__":
    main()
