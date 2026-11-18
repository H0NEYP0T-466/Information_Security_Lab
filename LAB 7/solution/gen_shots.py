#!/usr/bin/env python3
"""
Render terminal-style screenshots and diagrams for Lab 07 with Pillow.
Author: Muhammad Fezan (Fall-23-BSCS-466)
Course: Information Security Lab (7th Semester - Fall 2026)
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
            cur = "    "
        cur += ch
    out.append(cur)
    return out


def render_terminal(text, title, out_name, width=1080, font_size=14, pad=20):
    fnt = f(MONO, font_size)
    avail = width - 2 * pad
    raw = text.rstrip("\n").split("\n")
    lines = []
    for ln in raw:
        lines.extend(wrap_line(ln, fnt, avail))

    lh = int(font_size * 1.48)
    bar_h = 38
    h = bar_h + pad * 2 + lh * len(lines)

    img = Image.new("RGB", (width, h), BG)
    d = ImageDraw.Draw(img)

    # Window title bar with macOS-style controls
    d.rectangle([0, 0, width, bar_h], fill=BAR)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 20 + i * 20
        d.ellipse([cx - 6, bar_h // 2 - 6, cx + 6, bar_h // 2 + 6], fill=col)
    d.text((width // 2, bar_h // 2), title, font=f(MONO, 12),
           fill=(170, 175, 182), anchor="mm")

    y = bar_h + pad
    for line in lines:
        s = line.strip()
        if s.startswith("====") or s.startswith("----") or s.startswith("+===") or s.startswith("+---"):
            d.text((pad, y), line, font=fnt, fill=DIM)
        elif s.startswith("TASK") or "SUCCESS" in s or "PASSED" in s:
            d.text((pad, y), line, font=f(MONO_B, font_size), fill=GREEN)
        elif s.startswith("[Step") or s.startswith("NETWORK STATUS"):
            d.text((pad, y), line, font=f(MONO_B, font_size), fill=YELLOW)
        elif s.startswith("[+]"):
            d.text((pad, y), line, font=f(MONO_B, font_size), fill=GREEN)
        elif s.startswith("[*]") or s.startswith("[=]"):
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
                vc = GREEN if "True" in val or "PASSED" in val else WHITE
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
    W, H = 1180, 380
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fm = f(MONO, 12)
    fmb = f(MONO_B, 12)

    d.text((36, 18), "Blockchain Mining Reward Architecture", font=f(SANS_B, 20), fill=GREEN_D)
    d.text((36, 46), "Every mined block includes an incentivizing coinbase reward (+50 coins) credited to miner address",
           font=fm, fill=GREY)

    # Box 1: Previous Block Link
    bx1 = 36
    d.rounded_rectangle([bx1, 80, bx1 + 240, 340], radius=8, fill=(245, 245, 247), outline=GREY, width=2)
    d.text((bx1 + 16, 96), "Block #(N-1)", font=f(SANS_B, 15), fill=INK)
    d.text((bx1 + 16, 122), "Index: N-1", font=fm, fill=GREY)
    d.text((bx1 + 16, 146), "Nonce: 248", font=fm, fill=GREY)
    d.rounded_rectangle([bx1 + 14, 180, bx1 + 226, 245], radius=5, fill=(232, 235, 240), outline=NAVY, width=1)
    d.text((bx1 + 20, 192), "SHA-256 Hash:", font=fm, fill=NAVY)
    d.text((bx1 + 20, 216), "00aef6ddd5...", font=fmb, fill=NAVY)
    d.text((bx1 + 16, 275), "Status: Verified", font=fm, fill=GREEN_D)

    # Arrow 1 -> 2
    d.line([bx1 + 240, 210, bx1 + 290, 210], fill=GREEN_M, width=3)
    d.polygon([(bx1 + 295, 210), (bx1 + 285, 204), (bx1 + 285, 216)], fill=GREEN_M)

    # Box 2: New Block
    bx2 = 300
    d.rounded_rectangle([bx2, 80, bx2 + 430, 340], radius=8, fill=(235, 245, 235), outline=GREEN_D, width=2)
    d.text((bx2 + 18, 96), "New Block #N (Coinbase)", font=f(SANS_B, 15), fill=GREEN_D)
    d.text((bx2 + 18, 122), "Previous Hash: 00aef6ddd5...", font=fm, fill=GREY)

    d.rounded_rectangle([bx2 + 16, 150, bx2 + 414, 255], radius=6, fill=(255, 252, 235), outline=AMBER, width=2)
    d.text((bx2 + 26, 162), "[Coinbase Payload]", font=f(SANS_B, 13), fill=AMBER)
    d.text((bx2 + 26, 188), "Type  : Mining_Reward", font=fm, fill=INK)
    d.text((bx2 + 26, 210), "Miner : 0x71A4_Alice_Miner", font=fmb, fill=NAVY)
    d.text((bx2 + 26, 232), "Amount: +50.0 Coins", font=fmb, fill=GREEN_D)

    d.text((bx2 + 18, 275), "Proof-of-Work: Nonce = 239 | Target = '00'", font=fm, fill=INK)
    d.text((bx2 + 18, 300), "New Hash: 0022ec75fd... (Valid)", font=fmb, fill=GREEN_D)

    # Arrow 2 -> 3
    d.line([bx2 + 430, 210, bx2 + 480, 210], fill=GREEN_M, width=3)
    d.polygon([(bx2 + 485, 210), (bx2 + 475, 204), (bx2 + 475, 216)], fill=GREEN_M)

    # Box 3: Wallet Ledger
    bx3 = 790
    d.rounded_rectangle([bx3, 80, W - 36, 340], radius=8, fill=(235, 241, 250), outline=NAVY, width=2)
    d.text((bx3 + 18, 96), "Miner Wallet Ledger", font=f(SANS_B, 15), fill=NAVY)
    d.text((bx3 + 18, 122), "Distributed State Balance:", font=fm, fill=GREY)

    wallets = [
        ("0x71A4_Alice_Miner", "+50.00", "100.00 coins", GREEN_D),
        ("0x94B2_Bob_Miner", "+50.00", "50.00 coins", GREEN_D),
        ("0x466F_Fezan_Miner", "+50.00", "50.00 coins", GREEN_D),
    ]
    for i, (addr, delta, tot, c) in enumerate(wallets):
        yy = 150 + i * 48
        d.rounded_rectangle([bx3 + 14, yy, W - 50, yy + 40], radius=5, fill=(255, 255, 255), outline=(210, 218, 230))
        d.text((bx3 + 22, yy + 5), addr[:17] + "..", font=fmb, fill=INK)
        d.text((bx3 + 22, yy + 22), f"Delta: {delta}", font=fm, fill=c)
        d.text((W - 155, yy + 12), tot, font=fmb, fill=NAVY)

    d.text((bx3 + 18, 305), "Ledger Balance: 200.00 Total Coins", font=fmb, fill=GREEN_D)

    d.rectangle([0, 0, W - 1, H - 1], outline=(210, 215, 210))
    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


def render_p2p_sync_diagram(out_name="diagram_p2p_sync.png"):
    W, H = 1180, 420
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fm = f(MONO, 12)
    fmb = f(MONO_B, 12)

    d.text((36, 18), "P2P Blockchain Network Synchronization & Nakamoto Consensus",
           font=f(SANS_B, 20), fill=GREEN_D)
    d.text((36, 46), "Nodes independently maintain chain copies and converge onto the longest cryptographically valid branch",
           font=fm, fill=GREY)

    n_boxes = [
        ("Node 1 (Miner)", 80, 85, 440, 220, GREEN_D, (232, 245, 233), "Mines Block #1 (Height: 2)", "002748bad3..."),
        ("Node 2 (Peer)", 720, 85, 1080, 220, NAVY, (235, 241, 250), "Adopts Node1 Chain (Height: 2)", "002748bad3..."),
        ("Node 3 (Peer)", 400, 260, 760, 395, AMBER, (255, 250, 235), "Adopts Node1 Chain (Height: 2)", "002748bad3..."),
    ]

    for title, x0, y0, x1, y1, border, bg, desc, tip in n_boxes:
        d.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=bg, outline=border, width=2)
        d.text((x0 + 16, y0 + 12), title, font=f(SANS_B, 14), fill=border)
        d.text((x0 + 16, y0 + 36), desc, font=fm, fill=INK)
        d.text((x0 + 16, y0 + 58), f"Tip Hash: {tip}", font=fmb, fill=border)
        d.line([x0 + 16, y0 + 82, x1 - 16, y0 + 82], fill=(210, 215, 220), width=1)
        d.text((x0 + 16, y0 + 92), "Rule: Longest Valid Chain (Nakamoto)", font=fm, fill=GREY)
        d.text((x0 + 16, y0 + 112), "Validation: SHA-256 + PoW Verified", font=fm, fill=GREEN_M)

    # Arrows
    d.line([440, 150, 720, 150], fill=GREEN_M, width=3)
    d.polygon([(720, 150), (708, 144), (708, 156)], fill=GREEN_M)
    d.text((530, 128), "sync_with_node()", font=fmb, fill=GREEN_D)

    d.line([260, 220, 420, 260], fill=GREEN_M, width=3)
    d.polygon([(420, 260), (408, 250), (414, 264)], fill=GREEN_M)

    d.line([900, 220, 740, 260], fill=AMBER, width=2)
    d.polygon([(740, 260), (752, 250), (748, 264)], fill=AMBER)

    d.rectangle([0, 0, W - 1, H - 1], outline=(210, 215, 210))
    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(HERE, "out1.txt"), encoding="utf-8") as f1:
        render_terminal(f1.read(), "task1_mining_rewards.py  -  Mining Rewards & Wallets", "shot_task1.png")
    with open(os.path.join(HERE, "out2.txt"), encoding="utf-8") as f2:
        render_terminal(f2.read(), "task2_p2p_network.py  -  Peer-to-Peer Synchronization", "shot_task2.png")
    render_mining_reward_diagram()
    render_p2p_sync_diagram()
