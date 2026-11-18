#!/usr/bin/env python3
"""
Render terminal-style screenshots and diagrams for Lab 07 with Pillow.
Author: Muhammad Fezan (Fall-23-BSCS-466)
Course: Information Security Lab (7th Semester - Fall 2026)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Lahore Garrison University
"""

import os
import re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "shots")

MONO = "/home/honeypot/.local/share/fonts/JetBrains/JetBrainsMonoNerdFont-Regular.ttf"
MONO_B = "/usr/share/fonts/liberation/LiberationMono-Bold.ttf"
SANS = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

# Terminal palette
BG = (30, 32, 36)
BAR = (44, 47, 52)
FG = (220, 223, 228)
DIM = (120, 126, 134)
GREEN = (126, 211, 122)
CYAN = (110, 200, 220)
YELLOW = (230, 200, 120)
RED = (235, 120, 120)
WHITE = (245, 246, 248)

# Document palette
INK = (33, 33, 33)
GREEN_D = (27, 94, 32)
GREEN_M = (46, 125, 50)
AMBER = (180, 140, 20)
NAVY = (26, 35, 126)
GREY = (90, 90, 90)


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap_line(line, fnt, avail):
    if fnt.getlength(line) <= avail:
        return [line]
    out, cur = [], ""
    for ch in line:
        if fnt.getlength(cur + ch) > avail:
            out.append(cur)
            cur = "        "
        cur += ch
    out.append(cur)
    return out


def render_terminal(text, title, out_name, width=1100, font_size=15, pad=24):
    fnt = f(MONO, font_size)
    avail = width - 2 * pad
    raw = text.rstrip("\n").split("\n")
    lines = []
    for ln in raw:
        lines.extend(wrap_line(ln, fnt, avail))

    lh = int(font_size * 1.50)
    bar_h = 42
    h = bar_h + pad * 2 + lh * len(lines)

    img = Image.new("RGB", (width, h), BG)
    d = ImageDraw.Draw(img)

    # Window title bar with macOS-style controls
    d.rectangle([0, 0, width, bar_h], fill=BAR)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 22 + i * 22
        d.ellipse([cx - 7, bar_h // 2 - 7, cx + 7, bar_h // 2 + 7], fill=col)
    d.text((width // 2, bar_h // 2), title, font=f(MONO, 13),
           fill=(170, 175, 182), anchor="mm")

    y = bar_h + pad
    for line in lines:
        s = line.strip()
        if s.startswith("====") or s.startswith("----") or s.startswith("+===") or s.startswith("+---"):
            d.text((pad, y), line, font=fnt, fill=DIM)
        elif s.startswith("TASK") or "SUCCESS" in s or "PASSED" in s:
            d.text((pad, y), line, font=f(MONO_B, font_size), fill=GREEN)
        elif s.startswith("[Step") or s.startswith("--- Mining") or s.startswith("-- State"):
            d.text((pad, y), line, font=f(MONO_B, font_size), fill=YELLOW)
        elif s.startswith("[+]"):
            d.text((pad, y), line, font=f(MONO_B, font_size), fill=GREEN)
        elif s.startswith("[*]"):
            d.text((pad, y), line, font=fnt, fill=CYAN)
        elif s.startswith("[-]"):
            d.text((pad, y), line, font=fnt, fill=RED)
        else:
            m = re.match(r"^(\s*)([^:]{1,36}?)(\s*:\s*)(.*)$", line)
            if m and m.group(2).strip():
                ind, label, sep, val = m.groups()
                x = pad
                d.text((x, y), ind + label + sep, font=fnt, fill=CYAN)
                x += fnt.getlength(ind + label + sep)
                vc = GREEN if val.strip() in ("True", "SUCCESS", "PASSED (100% Agreement)") else WHITE
                d.text((x, y), val, font=fnt, fill=vc)
            elif "|" in line:
                d.text((pad, y), line, font=fnt, fill=WHITE)
            else:
                d.text((pad, y), line, font=fnt, fill=FG)
        y += lh

    d.rectangle([0, 0, width - 1, h - 1], outline=(58, 62, 68))
    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


def render_mining_reward_diagram(out_name="diagram_mining_reward.png"):
    W, H = 1180, 480
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fm = f(MONO, 13)
    fmb = f(MONO_B, 13)

    d.text((36, 22), "Blockchain Mining Reward & Coinbase Transaction Architecture",
           font=f(SANS_B, 22), fill=GREEN_D)
    d.text((36, 56), "Every mined block includes an incentivizing coinbase reward (+50 coins) credited to miner address",
           font=fm, fill=GREY)

    # Box 1: Previous Block Link
    bx1 = 36
    d.rounded_rectangle([bx1, 100, bx1 + 240, 410], radius=8, fill=(245, 245, 247),
                        outline=GREY, width=2)
    d.text((bx1 + 16, 116), "Block #(N-1)", font=f(SANS_B, 16), fill=INK)
    d.text((bx1 + 16, 142), "Index: N-1", font=fm, fill=GREY)
    d.text((bx1 + 16, 166), "Nonce: 379", font=fm, fill=GREY)
    d.text((bx1 + 16, 196), "State Root: Valid", font=fm, fill=GREEN_M)
    d.rounded_rectangle([bx1 + 14, 230, bx1 + 226, 300], radius=5, fill=(232, 235, 240), outline=NAVY, width=1)
    d.text((bx1 + 22, 242), "Block Hash (SHA-256):", font=fm, fill=NAVY)
    d.text((bx1 + 22, 268), "00d057de596c...", font=fmb, fill=NAVY)
    d.text((bx1 + 16, 330), "Status: Finalized", font=fm, fill=GREEN_D)
    d.text((bx1 + 16, 356), "Chained to Ledger", font=fm, fill=GREY)

    # Arrow 1 -> 2
    d.line([bx1 + 240, 265, bx1 + 290, 265], fill=GREEN_M, width=3)
    d.polygon([(bx1 + 295, 265), (bx1 + 285, 258), (bx1 + 285, 272)], fill=GREEN_M)

    # Box 2: New Mined Block with Reward Payload
    bx2 = 300
    d.rounded_rectangle([bx2, 100, bx2 + 420, 410], radius=8, fill=(235, 245, 235),
                        outline=GREEN_D, width=2)
    d.text((bx2 + 18, 116), "New Block #N (Coinbase)", font=f(SANS_B, 16), fill=GREEN_D)
    d.text((bx2 + 18, 142), "Previous Hash: 00d057de596c...", font=fm, fill=GREY)
    d.text((bx2 + 18, 166), "Timestamp: UTC Mon Nov 18", font=fm, fill=GREY)

    # Inner Payload Box (Reward)
    d.rounded_rectangle([bx2 + 18, 195, bx2 + 402, 310], radius=6, fill=(255, 252, 235),
                        outline=AMBER, width=2)
    d.text((bx2 + 28, 208), "[Coinbase Transaction Payload]", font=f(SANS_B, 14), fill=AMBER)
    d.text((bx2 + 28, 234), "Type   : Mining_Reward", font=fm, fill=INK)
    d.text((bx2 + 28, 258), "Miner  : 0x71A4_Alice_Miner", font=fmb, fill=NAVY)
    d.text((bx2 + 28, 282), "Amount : +50.0 Coins", font=fmb, fill=GREEN_D)

    d.text((bx2 + 18, 330), "Proof-of-Work: Nonce = 379", font=fm, fill=INK)
    d.text((bx2 + 18, 356), "Computed Hash: 00438e73030a... (Valid)", font=fmb, fill=GREEN_D)
    d.text((bx2 + 18, 380), "Difficulty: Target '00' (2 leading zeros)", font=fm, fill=GREY)

    # Arrow 2 -> 3
    d.line([bx2 + 420, 265, bx2 + 470, 265], fill=GREEN_M, width=3)
    d.polygon([(bx2 + 475, 265), (bx2 + 465, 258), (bx2 + 465, 272)], fill=GREEN_M)

    # Box 3: Distributed State & Miner Wallet Ledger
    bx3 = 780
    d.rounded_rectangle([bx3, 100, W - 36, 410], radius=8, fill=(235, 241, 250),
                        outline=NAVY, width=2)
    d.text((bx3 + 18, 116), "Miner Wallet Ledger", font=f(SANS_B, 16), fill=NAVY)
    d.text((bx3 + 18, 142), "State Transition on Block Commit:", font=fm, fill=GREY)

    # Ledger rows
    wallets = [
        ("0x71A4_Alice_Miner", "+50.00", "100.00 coins", GREEN_D),
        ("0x94B2_Bob_Miner", "--", "50.00 coins", GREY),
        ("0x466F_Fezan_Miner", "--", "50.00 coins", GREY),
    ]
    for i, (addr, delta, tot, c) in enumerate(wallets):
        yy = 175 + i * 55
        d.rounded_rectangle([bx3 + 16, yy, W - 52, yy + 46], radius=5, fill=(255, 255, 255), outline=(210, 218, 230))
        d.text((bx3 + 24, yy + 6), addr[:18] + "..", font=fmb, fill=INK)
        d.text((bx3 + 24, yy + 26), f"Delta: {delta}", font=fm, fill=c)
        d.text((W - 165, yy + 14), tot, font=fmb, fill=NAVY)

    d.text((bx3 + 18, 352), "Ledger Invariant: Sum(Wallets) ==", font=fm, fill=INK)
    d.text((bx3 + 18, 376), "Total Mined Blocks * 50 Coins", font=fmb, fill=GREEN_D)

    d.rectangle([0, 0, W - 1, H - 1], outline=(210, 215, 210))
    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


def render_p2p_sync_diagram(out_name="diagram_p2p_sync.png"):
    W, H = 1180, 520
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fm = f(MONO, 13)
    fmb = f(MONO_B, 13)

    d.text((36, 20), "P2P Blockchain Network Synchronization & Nakamoto Consensus",
           font=f(SANS_B, 22), fill=GREEN_D)
    d.text((36, 54), "Nodes independently maintain chain copies and converge onto the longest cryptographically valid branch",
           font=fm, fill=GREY)

    # Node positions
    # Node1 (Top Center/Left), Node2 (Bottom Left), Node3 (Bottom Right)
    n_boxes = [
        ("Node 1 (Miner)", 100, 100, 480, 260, GREEN_D, (232, 245, 233), "Mines Block #1 (Height: 2)", "0099faae50f9f7..."),
        ("Node 2 (Peer)", 680, 100, 1060, 260, NAVY, (235, 241, 250), "Adopts Node1 Chain (Height: 2)", "0099faae50f9f7..."),
        ("Node 3 (Peer)", 390, 310, 770, 470, AMBER, (255, 250, 235), "Adopts Node1 Chain (Height: 2)", "0099faae50f9f7..."),
    ]

    for title, x0, y0, x1, y1, border, bg, desc, tip in n_boxes:
        d.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=bg, outline=border, width=2)
        d.text((x0 + 16, y0 + 14), title, font=f(SANS_B, 16), fill=border)
        d.text((x0 + 16, y0 + 40), desc, font=fm, fill=INK)
        d.text((x0 + 16, y0 + 64), f"Tip Hash: {tip}", font=fmb, fill=border)
        d.line([x0 + 16, y0 + 92, x1 - 16, y0 + 92], fill=(210, 215, 220), width=1)
        d.text((x0 + 16, y0 + 102), "Consensus Rule: Longest Valid Chain", font=fm, fill=GREY)
        d.text((x0 + 16, y0 + 126), "Validation: SHA-256 + PoW Verification", font=fm, fill=GREEN_M)

    # Sync propagation arrows
    # Node 1 -> Node 2
    d.line([480, 180, 680, 180], fill=GREEN_M, width=3)
    d.polygon([(680, 180), (666, 173), (666, 187)], fill=GREEN_M)
    d.text((515, 155), "sync_with_node()", font=fmb, fill=GREEN_D)

    # Node 1 -> Node 3
    d.line([290, 260, 450, 310], fill=GREEN_M, width=3)
    d.polygon([(450, 310), (436, 301), (442, 314)], fill=GREEN_M)
    d.text((250, 280), "sync_with_node()", font=fmb, fill=GREEN_D)

    # Node 2 <-> Node 3
    d.line([870, 260, 710, 310], fill=AMBER, width=2)
    d.polygon([(710, 310), (724, 301), (718, 314)], fill=AMBER)
    d.text((790, 280), "P2P Gossip", font=fmb, fill=AMBER)

    d.rectangle([0, 0, W - 1, H - 1], outline=(210, 215, 210))
    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)

    with open(os.path.join(HERE, "out1.txt"), encoding="utf-8") as f1:
        render_terminal(f1.read(), "task1_mining_rewards.py  -  Blockchain Mining Rewards & Wallets", "shot_task1.png")

    with open(os.path.join(HERE, "out2.txt"), encoding="utf-8") as f2:
        render_terminal(f2.read(), "task2_p2p_network.py  -  Peer-to-Peer Synchronization & Consensus", "shot_task2.png")

    render_mining_reward_diagram()
    render_p2p_sync_diagram()
