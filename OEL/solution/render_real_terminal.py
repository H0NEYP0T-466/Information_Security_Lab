#!/usr/bin/env python3
"""
Render authentic Linux terminal window screenshots for OEL tasks.
Author: Muhammad Fezan (Fall-23-BSCS-466)
"""

import os
import re
import subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = "/home/honeypot/Univeristy_Data/IS(L)/OEL/solution"
OUT = os.path.join(HERE, "shots")
os.makedirs(OUT, exist_ok=True)

MONO = "/home/honeypot/.local/share/fonts/JetBrains/JetBrainsMonoNerdFont-Regular.ttf"
MONO_B = "/usr/share/fonts/liberation/LiberationMono-Bold.ttf"

# Authentic Dark Terminal Palette (One Dark / Alacritty theme)
BG = (20, 22, 26)
BAR = (33, 37, 43)
BORDER = (50, 55, 65)

# Text Colors
FG = (220, 224, 230)
DIM = (110, 116, 126)
GREEN = (90, 215, 120)
RED = (240, 100, 100)
CYAN = (95, 205, 235)
YELLOW = (235, 205, 110)
BLUE = (97, 175, 239)
PURPLE = (198, 120, 221)
WHITE = (250, 250, 252)


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


def render_terminal_window(cmd: str, raw_output: str, title: str, out_name: str,
                           width: int = 1100, font_size: int = 13, pad: int = 18):
    fnt = f(MONO, font_size)
    fnt_b = f(MONO_B, font_size)
    lh = int(font_size * 1.48)
    bar_h = 36

    avail = width - 2 * pad

    lines = []
    for ln in raw_output.strip("\n").split("\n"):
        lines.extend(wrap_line(ln, fnt, avail))

    total_display_lines = 1 + len(lines) + 1
    h = bar_h + pad * 2 + total_display_lines * lh

    img = Image.new("RGB", (width, h), BG)
    d = ImageDraw.Draw(img)

    # Window title bar with macOS/Linux style window controls
    d.rectangle([0, 0, width, bar_h], fill=BAR)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 18 + i * 18
        d.ellipse([cx - 5, bar_h // 2 - 5, cx + 5, bar_h // 2 + 5], fill=col)
    d.text((width // 2, bar_h // 2), title, font=f(MONO, 11.5), fill=(160, 165, 175), anchor="mm")

    # Render Opening Prompt
    y = bar_h + pad
    x = pad
    user_host = "honeypot@honeypot"
    d.text((x, y), user_host, font=fnt_b, fill=GREEN)
    x += fnt_b.getlength(user_host)

    d.text((x, y), ":", font=fnt, fill=FG)
    x += fnt.getlength(":")

    path_str = "~/Univeristy_Data/IS(L)/OEL"
    d.text((x, y), path_str, font=fnt_b, fill=BLUE)
    x += fnt_b.getlength(path_str)

    d.text((x, y), "$ ", font=fnt_b, fill=WHITE)
    x += fnt_b.getlength("$ ")

    d.text((x, y), cmd, font=fnt_b, fill=WHITE)
    y += lh

    # Render Body Output
    for line in lines:
        s = line.strip()
        x = pad
        if s.startswith("====") or s.startswith("----") or s.startswith("+===") or s.startswith("+---"):
            d.text((x, y), line, font=fnt, fill=DIM)
        elif s.startswith("PART") or "PASSED" in s or "INTEGRITY VERIFIED" in s:
            d.text((x, y), line, font=fnt_b, fill=GREEN)
        elif s.startswith("[Mining]") or s.startswith("[Adversary Action]") or s.startswith("[Current") or s.startswith("[Modified"):
            d.text((x, y), line, font=fnt_b, fill=YELLOW)
        elif s.startswith("[+]"):
            d.text((x, y), line, font=fnt_b, fill=GREEN)
        elif s.startswith("[-]"):
            d.text((x, y), line, font=fnt_b, fill=RED)
        elif s.startswith("[51% Attack]"):
            d.text((x, y), line, font=fnt, fill=PURPLE)
        elif "True" in s:
            parts = line.split("True", 1)
            d.text((x, y), parts[0], font=fnt, fill=FG)
            x_t = x + fnt.getlength(parts[0])
            d.text((x_t, y), "True", font=fnt_b, fill=GREEN)
            x_t += fnt_b.getlength("True")
            d.text((x_t, y), parts[1], font=fnt, fill=FG)
        elif "False" in s:
            parts = line.split("False", 1)
            d.text((x, y), parts[0], font=fnt, fill=FG)
            x_f = x + fnt.getlength(parts[0])
            d.text((x_f, y), "False", font=fnt_b, fill=RED)
            x_f += fnt_b.getlength("False")
            d.text((x_f, y), parts[1], font=fnt, fill=FG)
        elif ":" in line and not line.startswith(" "):
            parts = line.split(":", 1)
            d.text((x, y), parts[0] + ":", font=fnt, fill=CYAN)
            d.text((x + fnt.getlength(parts[0] + ": "), y), parts[1], font=fnt, fill=FG)
        elif line.startswith("    ") and ":" in line:
            parts = line.split(":", 1)
            d.text((x, y), parts[0] + ":", font=fnt, fill=CYAN)
            d.text((x + fnt.getlength(parts[0] + ": "), y), parts[1], font=fnt, fill=FG)
        else:
            d.text((x, y), line, font=fnt, fill=FG)
        y += lh

    # Render Trailing Prompt with Cursor
    x = pad
    d.text((x, y), user_host, font=fnt_b, fill=GREEN)
    x += fnt_b.getlength(user_host)
    d.text((x, y), ":", font=fnt, fill=FG)
    x += fnt.getlength(":")
    d.text((x, y), path_str, font=fnt_b, fill=BLUE)
    x += fnt_b.getlength(path_str)
    d.text((x, y), "$ ", font=fnt_b, fill=WHITE)
    x += fnt_b.getlength("$ ")
    d.text((x, y), "█", font=fnt, fill=WHITE)

    # Window border
    d.rectangle([0, 0, width - 1, h - 1], outline=BORDER, width=1)

    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print(f"Rendered Real Terminal: {path} ({width}x{h})")
    return path


if __name__ == "__main__":
    venv_py = "/home/honeypot/.hermes/hermes-agent/venv/bin/python"
    script = os.path.join(HERE, "blockchain_oel.py")

    # Run Part 1
    out1 = subprocess.check_output([venv_py, script, "1"]).decode("utf-8")
    render_terminal_window("python3 blockchain_oel.py 1", out1,
                           "honeypot@honeypot: ~/Univeristy_Data/IS(L)/OEL — Task 1: PoW Mining",
                           "shot_q1_terminal.png")

    # Run Part 2
    out2 = subprocess.check_output([venv_py, script, "2"]).decode("utf-8")
    render_terminal_window("python3 blockchain_oel.py 2", out2,
                           "honeypot@honeypot: ~/Univeristy_Data/IS(L)/OEL — Task 2: Chain Validation",
                           "shot_q2_terminal.png")

    # Run Part 3
    out3 = subprocess.check_output([venv_py, script, "3"]).decode("utf-8")
    render_terminal_window("python3 blockchain_oel.py 3", out3,
                           "honeypot@honeypot: ~/Univeristy_Data/IS(L)/OEL — Task 3: Tampering Simulation",
                           "shot_q3_terminal.png")

    # Run Part 4
    out4 = subprocess.check_output([venv_py, script, "4"]).decode("utf-8")
    render_terminal_window("python3 blockchain_oel.py 4", out4,
                           "honeypot@honeypot: ~/Univeristy_Data/IS(L)/OEL — Task 4: 51% Attack Simulation",
                           "shot_q4_terminal.png")
