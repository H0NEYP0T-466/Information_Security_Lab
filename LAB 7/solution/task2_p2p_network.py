#!/usr/bin/env python3
"""
Information Security Lab - Week 07
Task 2: Basic Blockchain Peer-to-Peer (P2P) Network Simulation
Author: Muhammad Fezan (Fall-23-BSCS-466)
Course: Information Security Lab (7th Semester - Fall 2026)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Lahore Garrison University - Department of Computer Science
"""

import copy
import time
import hashlib
import json
from typing import List, Dict, Any, Optional


class Block:
    """Represents an immutable, timestamped block in the ledger."""

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
        target_prefix = "0" * difficulty
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.compute_hash()


class Blockchain:
    """Manages an individual node's private copy of the distributed ledger."""

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty: int = difficulty
        self.mining_reward: float = 50.0
        self.wallets: Dict[str, float] = {}
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis_block = Block(
            index=0,
            timestamp=1763450000.0,
            data={"type": "Genesis", "message": "Genesis Block - LGU P2P"},
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
            "block_index": new_index
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
        return new_block

    def is_chain_valid(self, chain_to_check: Optional[List[Block]] = None) -> bool:
        target_chain = chain_to_check if chain_to_check is not None else self.chain
        target_prefix = "0" * self.difficulty
        for i in range(1, len(target_chain)):
            curr = target_chain[i]
            prev = target_chain[i - 1]
            if curr.hash != curr.compute_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
            if not curr.hash.startswith(target_prefix):
                return False
        return True


class Node:
    """Represents an autonomous peer node operating in the P2P network."""

    def __init__(self, node_name: str, difficulty: int = 2):
        self.node_name: str = node_name
        self.blockchain: Blockchain = Blockchain(difficulty=difficulty)

    def sync_with_node(self, peer_node: "Node") -> bool:
        """Synchronizes blockchain with a peer using Nakamoto Longest Chain Rule."""
        peer_chain = peer_node.blockchain.chain
        if not self.blockchain.is_chain_valid(peer_chain):
            print(f"[-] [{self.node_name}] Rejected sync: Peer [{peer_node.node_name}] chain is invalid!")
            return False

        if len(peer_chain) > len(self.blockchain.chain):
            old_len = len(self.blockchain.chain)
            self.blockchain.chain = copy.deepcopy(peer_chain)
            self.blockchain.wallets = copy.deepcopy(peer_node.blockchain.wallets)
            print(f"[+] [{self.node_name}] Synced with [{peer_node.node_name}] | Length: {old_len} -> {len(self.blockchain.chain)} | Tip: {self.blockchain.get_latest_block().hash[:18]}..")
            return True
        else:
            print(f"[=] [{self.node_name}] Already up-to-date with [{peer_node.node_name}] (Length: {len(self.blockchain.chain)})")
            return False


def display_network_matrix(nodes: List[Node], phase_name: str) -> bool:
    """Displays synchronized status matrix of all nodes in the network."""
    base_len = len(nodes[0].blockchain.chain)
    base_hash = nodes[0].blockchain.get_latest_block().hash

    print("\n" + "=" * 68)
    print(f"        NETWORK STATUS MATRIX - {phase_name.upper()}")
    print("=" * 68)
    print(f"{'Node Name':<12} | {'Blocks':<8} | {'Valid':<7} | {'Latest Block Hash':<32}")
    print("-" * 68)

    all_synced = True
    for n in nodes:
        c_len = len(n.blockchain.chain)
        c_val = n.blockchain.is_chain_valid()
        l_hash = n.blockchain.get_latest_block().hash
        if c_len != base_len or l_hash != base_hash:
            all_synced = False
        print(f"{n.node_name:<12} | {c_len:<8} | {str(c_val):<7} | {l_hash[:30]}..")

    print("-" * 68)
    status_str = "PASSED (100% Agreement)" if all_synced else "DIVERGENT (Sync Required)"
    print(f"Network Convergence: {status_str}")
    print("=" * 68)
    return all_synced


def main():
    print("=" * 68)
    print(" TASK 2: BASIC BLOCKCHAIN PEER-TO-PEER (P2P) NETWORK SIMULATION")
    print(" Author: Muhammad Fezan (Fall-23-BSCS-466) | Course: IS(L)")
    print("=" * 68)

    # 1. Initialize three nodes
    print("\n[Step 1] Initializing three independent nodes: Node1, Node2, Node3...")
    node1 = Node("Node1")
    node2 = Node("Node2")
    node3 = Node("Node3")
    nodes = [node1, node2, node3]
    display_network_matrix(nodes, "Initial State (Genesis)")

    # 2. Mine on Node1
    print("\n[Step 2] Mining new Block #1 on Node1 (Miner: 0xNode1_Miner)...")
    node1.blockchain.mine_block("0xNode1_Miner")
    display_network_matrix(nodes, "Post-Mining (Node1 Ahead)")

    # 3. Synchronize Node2 and Node3 with Node1
    print("\n[Step 3] Synchronizing Node2 and Node3 with Node1...")
    node2.sync_with_node(node1)
    node3.sync_with_node(node1)

    # 4. Display & Verify after synchronization
    print("\n[Step 4] Network status after Phase 1 synchronization:")
    display_network_matrix(nodes, "Phase 1 Synchronized")

    # 5. Round 2: Mine on Node2 and propagate
    print("\n[Step 5] Mining new Block #2 on Node2 (Miner: 0xNode2_Miner)...")
    node2.blockchain.mine_block("0xNode2_Miner")
    display_network_matrix(nodes, "Post-Mining (Node2 Ahead)")

    print("\n[Step 6] Synchronizing Node1 and Node3 with Node2...")
    node1.sync_with_node(node2)
    node3.sync_with_node(node2)

    # 6. Final verification
    print("\n[Step 7] Final Network State across all nodes:")
    success = display_network_matrix(nodes, "Final Network State")
    print(f"\nFinal P2P Convergence Status: {'SUCCESS' if success else 'FAILURE'}")


if __name__ == "__main__":
    main()
