#!/usr/bin/env python3
"""
Information Security Lab - Week 07
Task 2: Basic Blockchain Peer-to-Peer (P2P) Network Simulation
Author: Muhammad Fezan (Fall-23-BSCS-466)
Course: Information Security Lab (7th Semester - Fall 2026)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Lahore Garrison University - Department of Computer Science

Objective:
    Simulate a decentralized peer-to-peer (P2P) blockchain network comprising
    multiple autonomous nodes (Node1, Node2, Node3). Demonstrate mining on an
    individual node, peer synchronization using the Longest Chain (Nakamoto)
    consensus rule, and ledger convergence across all participants.
"""

import copy
import time
import hashlib
import json
from typing import List, Dict, Any, Optional


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
        """Finds a nonce satisfying target difficulty."""
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
        """Initializes blockchain with common Genesis block."""
        genesis_block = Block(
            index=0,
            timestamp=1763450000.0,
            data={"type": "Genesis", "message": "Genesis Block - LGU P2P Network"},
            previous_hash="0" * 64,
            nonce=0
        )
        genesis_block.proof_of_work(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mine_block(self, miner_address: str) -> Block:
        """Mines a new block and appends it locally."""
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
        """Verifies cryptographic integrity of the given or local chain."""
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
    """
    Represents an autonomous peer node operating in the P2P network.
    Maintains an independent local replica of the blockchain and communicates
    with peer nodes via synchronization protocols.
    """

    def __init__(self, node_name: str, difficulty: int = 2):
        self.node_name: str = node_name
        self.blockchain: Blockchain = Blockchain(difficulty=difficulty)

    def sync_with_node(self, peer_node: "Node") -> bool:
        """
        Synchronizes local blockchain ledger with a peer node.
        Applies Nakamoto Consensus:
        1. Peer chain must be cryptographically valid.
        2. Peer chain must be strictly longer than local chain.
        If both hold, adopts peer's chain.
        """
        peer_chain = peer_node.blockchain.chain

        print(f"[*] [{self.node_name}] Initiating P2P sync with [{peer_node.node_name}]...")
        print(f"    Local Chain Length: {len(self.blockchain.chain)} | Peer Chain Length: {len(peer_chain)}")

        # 1. Validate peer chain integrity
        if not self.blockchain.is_chain_valid(peer_chain):
            print(f"    [-] Sync rejected: Peer [{peer_node.node_name}] chain is invalid!")
            return False

        # 2. Apply Longest Chain Rule
        if len(peer_chain) > len(self.blockchain.chain):
            old_len = len(self.blockchain.chain)
            # Perform deep copy to ensure full memory isolation between peer nodes
            self.blockchain.chain = copy.deepcopy(peer_chain)
            self.blockchain.wallets = copy.deepcopy(peer_node.blockchain.wallets)
            print(f"    [+] SUCCESS: [{self.node_name}] adopted longer chain from [{peer_node.node_name}]!")
            print(f"        Blocks updated: {old_len} -> {len(self.blockchain.chain)}")
            print(f"        Latest Block Hash: {self.blockchain.get_latest_block().hash[:24]}...")
            return True
        else:
            print(f"    [=] No update needed: Local chain is already equal or longer than peer's.")
            return False

    def display_node_chain(self) -> None:
        """Prints a structured summary of the node's local blockchain copy."""
        print(f"\n+{'='*66}+")
        print(f"| Node: {self.node_name:<20} | Total Blocks: {len(self.blockchain.chain):<4} | Valid: {self.blockchain.is_chain_valid():<5} |")
        print(f"+{'-'*66}+")
        print(f"| {'Idx':<4} | {'Miner / Data':<24} | {'Nonce':<6} | {'Hash (prefix)':<22} |")
        print(f"+{'-'*66}+")
        for b in self.blockchain.chain:
            beneficiary = b.data.get("miner", b.data.get("type", "Block"))
            h_preview = b.hash[:20] + ".."
            print(f"| {b.index:<4} | {beneficiary:<24} | {b.nonce:<6} | {h_preview:<22} |")
        print(f"+{'='*66}+")


def verify_network_convergence(nodes: List[Node]) -> bool:
    """Verifies that all nodes in the network have identical blockchain states."""
    if not nodes:
        return True

    base_len = len(nodes[0].blockchain.chain)
    base_latest_hash = nodes[0].blockchain.get_latest_block().hash

    print("\n" + "=" * 68)
    print("           P2P NETWORK CONVERGENCE VERIFICATION")
    print("=" * 68)
    print(f"{'Node Name':<12} | {'Chain Length':<14} | {'Latest Block Hash':<34}")
    print("-" * 68)

    all_matched = True
    for node in nodes:
        c_len = len(node.blockchain.chain)
        l_hash = node.blockchain.get_latest_block().hash
        matches = (c_len == base_len) and (l_hash == base_latest_hash)
        if not matches:
            all_matched = False
        print(f"{node.node_name:<12} | {c_len:<14} | {l_hash[:32]}..")

    print("-" * 68)
    print(f"Verification Result: {'ALL NODES SYNCHRONIZED AND IDENTICAL' if all_matched else 'DESYNCHRONIZATION DETECTED'}")
    print(f"Consensus Status   : {'PASSED (100% Agreement)' if all_matched else 'FAILED'}")
    print("=" * 68)
    return all_matched


def main():
    print("=" * 68)
    print(" TASK 2: BASIC BLOCKCHAIN PEER-TO-PEER (P2P) NETWORK SIMULATION")
    print(" Author: Muhammad Fezan (Fall-23-BSCS-466) | Course: IS(L)")
    print("=" * 68)

    # 1. Create three independent network nodes
    print("\n[Step 1] Initializing three independent P2P network nodes...")
    node1 = Node("Node1")
    node2 = Node("Node2")
    node3 = Node("Node3")
    nodes = [node1, node2, node3]
    print("         Created: Node1, Node2, Node3 (each holding isolated Genesis block)")

    # 2. Mine a new block on Node1
    print("\n[Step 2] Mining a new block on Node1 (Miner: 0xNode1_Miner)...")
    node1.blockchain.mine_block("0xNode1_Miner")

    print("\n-- State before network synchronization --")
    print(f"Node1 chain length: {len(node1.blockchain.chain)} blocks (Genesis + Mined Block #1)")
    print(f"Node2 chain length: {len(node2.blockchain.chain)} blocks (Genesis only)")
    print(f"Node3 chain length: {len(node3.blockchain.chain)} blocks (Genesis only)")

    # 3. Synchronize Node2 and Node3 with Node1
    print("\n[Step 3] Propagating block and synchronizing Node2 and Node3 with Node1...")
    node2.sync_with_node(node1)
    node3.sync_with_node(node1)

    # 4. Display the blockchain of each node after synchronization
    print("\n[Step 4] Displaying blockchain ledger of each node after Phase 1 sync:")
    for n in nodes:
        n.display_node_chain()

    # 5. Verify all nodes contain the same number of blocks
    print("\n[Step 5] Phase 1 Verification:")
    verify_network_convergence(nodes)

    # 6. Advanced Round: Mine Block #2 on Node2, and synchronize across network
    print("\n[Step 6] Mining Block #2 on Node2 (Miner: 0xNode2_Miner)...")
    node2.blockchain.mine_block("0xNode2_Miner")
    print(f"Node2 chain length increased to {len(node2.blockchain.chain)} blocks.")

    print("\n[Step 7] Synchronizing Node1 and Node3 with Node2...")
    node1.sync_with_node(node2)
    node3.sync_with_node(node2)

    print("\n[Step 8] Final Network State:")
    for n in nodes:
        n.display_node_chain()

    # 7. Final Verification across all nodes
    print("\n[Step 9] Final P2P Consensus Verification:")
    success = verify_network_convergence(nodes)
    print(f"Simulation completed with status: {'SUCCESS' if success else 'FAILURE'}\n")


if __name__ == "__main__":
    main()
