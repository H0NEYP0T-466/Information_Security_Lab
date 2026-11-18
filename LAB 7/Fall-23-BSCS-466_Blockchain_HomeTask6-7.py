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
"""

import copy
import hashlib
import json
import time
from typing import Any, Dict, List, Optional


class Block:
    """Represents an immutable block in the blockchain ledger."""

    def __init__(self, index: int, timestamp: float, data: Dict[str, Any],
                 previous_hash: str = "", nonce: int = 0):
        self.index: int = index
        self.timestamp: float = timestamp
        self.data: Dict[str, Any] = data
        self.previous_hash: str = previous_hash
        self.nonce: int = nonce
        self.hash: str = self.compute_hash()

    def compute_hash(self) -> str:
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
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()


class Blockchain:
    """Manages chain, mining difficulty, and miner wallet balances."""

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty: int = difficulty
        self.mining_reward: float = 50.0  # Requirement: 50 coins mining reward
        self.wallets: Dict[str, float] = {}
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
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
        return self.chain[-1]

    def mine_block(self, miner_address: str) -> Block:
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
        new_block.proof_of_work(self.difficulty)
        self.chain.append(new_block)
        if miner_address not in self.wallets:
            self.wallets[miner_address] = 0.0
        self.wallets[miner_address] += self.mining_reward
        print(f"[+] Block #{new_index} mined by {miner_address} | Hash: {new_block.hash[:20]}.. | Reward: +50 coins")
        return new_block

    def is_chain_valid(self, chain_to_check: Optional[List[Block]] = None) -> bool:
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
        print("=" * 68)
        print("             MINER REWARDS AND WALLET BALANCES")
        print("=" * 68)
        print(f"{'Miner Address':<34} | {'Blocks':<8} | {'Total Reward':<16}")
        print("-" * 68)
        for miner, balance in sorted(self.wallets.items()):
            blocks = int(balance // self.mining_reward)
            print(f"{miner:<34} | {blocks:<8} | {balance:>10.2f} coins")
        print("-" * 68)
        print(f"Total Distributed: {sum(self.wallets.values()):.2f} coins across {len(self.wallets)} miners")
        print("=" * 68)


class Node:
    """Simulates an independent peer node holding a local blockchain instance."""

    def __init__(self, node_name: str, difficulty: int = 2):
        self.node_name: str = node_name
        self.blockchain: Blockchain = Blockchain(difficulty=difficulty)

    def sync_with_node(self, peer: "Node") -> bool:
        peer_chain = peer.blockchain.chain
        if not self.blockchain.is_chain_valid(peer_chain):
            return False
        if len(peer_chain) > len(self.blockchain.chain):
            old_len = len(self.blockchain.chain)
            self.blockchain.chain = copy.deepcopy(peer_chain)
            self.blockchain.wallets = copy.deepcopy(peer.blockchain.wallets)
            print(f"[+] [{self.node_name}] Synced with [{peer.node_name}] (Blocks: {old_len} -> {len(self.blockchain.chain)})")
            return True
        return False


def run_task1():
    print("\n" + "=" * 68)
    print(" TASK 1: SIMPLIFIED BLOCKCHAIN MINING REWARD SYSTEM")
    print("=" * 68)
    bc = Blockchain(difficulty=2)
    print(f"[Init] Blockchain created with Genesis Block. Reward: {bc.mining_reward} coins\n")
    bc.mine_block("0x71A4_Alice_Miner")
    bc.mine_block("0x94B2_Bob_Miner")
    bc.mine_block("0x71A4_Alice_Miner")
    print("\n[Ledger] Miner Rewards:")
    bc.print_rewards()
    print(f"\n[Verification] Chain Valid: {bc.is_chain_valid()} | Total Blocks: {len(bc.chain)}")


def run_task2():
    print("\n" + "=" * 68)
    print(" TASK 2: BASIC BLOCKCHAIN PEER-TO-PEER (P2P) NETWORK SIMULATION")
    print("=" * 68)
    node1 = Node("Node1")
    node2 = Node("Node2")
    node3 = Node("Node3")
    print("[Init] Node1, Node2, Node3 created.")
    print("[Mining] Node1 mining Block #1...")
    node1.blockchain.mine_block("0xNode1_Miner")
    print(f"Status before sync: Node1={len(node1.blockchain.chain)}, Node2={len(node2.blockchain.chain)}, Node3={len(node3.blockchain.chain)}")
    print("[Sync] Synchronizing Node2 and Node3 with Node1...")
    node2.sync_with_node(node1)
    node3.sync_with_node(node1)
    print(f"Status after sync : Node1={len(node1.blockchain.chain)}, Node2={len(node2.blockchain.chain)}, Node3={len(node3.blockchain.chain)}")
    same_len = len(node1.blockchain.chain) == len(node2.blockchain.chain) == len(node3.blockchain.chain)
    same_hash = node1.blockchain.get_latest_block().hash == node2.blockchain.get_latest_block().hash == node3.blockchain.get_latest_block().hash
    print(f"[Verification] All nodes synchronized: {same_len and same_hash}")


def main():
    print("=" * 68)
    print(" LAHORE GARRISON UNIVERSITY - DEPARTMENT OF COMPUTER SCIENCE")
    print(" Student: Muhammad Fezan | Roll No: Fall-23-BSCS-466")
    print("=" * 68)
    run_task1()
    run_task2()


if __name__ == "__main__":
    main()
