#!/usr/bin/env python3
"""Render terminal-style screenshots and diagrams for Lab 06 with Pillow."""

import os
import re
import math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "shots")

MONO = "/home/honeypot/.local/share/fonts/JetBrains/JetBrainsMonoNerdFont-Regular.ttf"
MONO_B = "/usr/share/fonts/liberation/LiberationMono-Bold.ttf"
SANS = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

# terminal palette
BG = (30, 32, 36)
BAR = (44, 47, 52)
FG = (220, 223, 228)
DIM = (120, 126, 134)
GREEN = (126, 211, 122)
CYAN = (110, 200, 220)
YELLOW = (230, 200, 120)
RED = (235, 120, 120)
WHITE = (245, 246, 248)

# document palette
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


def render_terminal(text, title, out_name, width=1080, font_size=16, pad=26):
    fnt = f(MONO, font_size)
    avail = width - 2 * pad
    raw = text.rstrip("\n").split("\n")
    lines = []
    for ln in raw:
        lines.extend(wrap_line(ln, fnt, avail))

    lh = int(font_size * 1.52)
    bar_h = 44
    h = bar_h + pad * 2 + lh * len(lines)

    img = Image.new("RGB", (width, h), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, width, bar_h], fill=BAR)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 22 + i * 22
        d.ellipse([cx - 7, bar_h // 2 - 7, cx + 7, bar_h // 2 + 7], fill=col)
    d.text((width // 2, bar_h // 2), title, font=f(MONO, 13),
           fill=(170, 175, 182), anchor="mm")

    y = bar_h + pad
    for line in lines:
        s = line.strip()
        if s.startswith("===="):
            d.text((pad, y), line, font=fnt, fill=DIM)
        elif s.startswith("TASK"):
            d.text((pad, y), line, font=f(MONO_B, font_size), fill=GREEN)
        elif s.startswith("--"):
            d.text((pad, y), line, font=f(MONO_B, font_size), fill=CYAN)
        elif "access denied" in s:
            d.text((pad, y), line, font=fnt, fill=RED)
        else:
            m = re.match(r"^(\s*)([^:]{1,40}?)(\s*:\s*)(.*)$", line)
            if m and m.group(2).strip():
                ind, label, sep, val = m.groups()
                x = pad
                d.text((x, y), ind + label + sep, font=fnt, fill=CYAN)
                x += fnt.getlength(ind + label + sep)
                vc = GREEN if val.strip() == "True" else WHITE
                d.text((x, y), val, font=fnt, fill=vc)
            else:
                d.text((pad, y), line, font=fnt, fill=FG)
        y += lh

    d.rectangle([0, 0, width - 1, h - 1], outline=(58, 62, 68))
    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


# ----------------------------------------------------------------------
def render_birthday_diagram(n_measured, p_measured, out_name="diagram_birthday.png"):
    W, H = 1180, 566
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fm = f(MONO, 14)

    d.text((34, 22), "Why 16 bits is not enough", font=f(SANS_B, 25), fill=GREEN_D)
    d.text((34, 58), "P(collision) = 1 - exp(-n(n-1) / 2^(b+1))    b = 16",
           font=fm, fill=GREY)

    # plot area
    x0, y0, x1, y1 = 90, 110, 700, 420
    d.rectangle([x0, y0, x1, y1], outline=(200, 205, 200))
    # grid
    for frac in (0.25, 0.5, 0.75, 1.0):
        yy = y1 - frac * (y1 - y0)
        d.line([x0, yy, x1, yy], fill=(232, 234, 230))
        d.text((x0 - 44, yy - 7), f"{int(frac * 100)}%", font=fm, fill=GREY)
    for n in range(0, 1001, 250):
        xx = x0 + n / 1000 * (x1 - x0)
        d.line([xx, y0, xx, y1], fill=(240, 241, 238))
        d.text((xx - 12, y1 + 8), str(n), font=fm, fill=GREY)
    d.text(((x0 + x1) / 2 - 40, y1 + 30), "messages hashed", font=fm, fill=INK)

    # curve
    pts = []
    for i in range(0, 1001):
        n = i
        p = 1 - math.exp(-n * (n - 1) / (2.0 ** 17))
        pts.append((x0 + n / 1000 * (x1 - x0), y1 - p * (y1 - y0)))
    d.line(pts, fill=GREEN_M, width=3)

    # 50% marker at 321
    xx = x0 + 321 / 1000 * (x1 - x0)
    d.line([xx, y0, xx, y1], fill=AMBER, width=1)
    d.ellipse([xx - 5, (y0 + y1) / 2 - 5, xx + 5, (y0 + y1) / 2 + 5], fill=AMBER)
    d.text((xx + 8, (y0 + y1) / 2 - 24), "321 msgs -> 50%", font=fm, fill=AMBER)

    # measured marker
    if n_measured and n_measured <= 1000:
        mx = x0 + n_measured / 1000 * (x1 - x0)
        my = y1 - p_measured / 100 * (y1 - y0)
        d.ellipse([mx - 6, my - 6, mx + 6, my + 6], outline=(200, 60, 60), width=3)
        d.text((mx - 162, my + 10), f"{n_measured} msgs -> {p_measured:.0f}%",
               font=fm, fill=(170, 40, 40))

    # right panel
    px = 740
    d.rounded_rectangle([px, 110, 1146, 236], radius=8, fill=(232, 245, 233),
                        outline=GREEN_M, width=2)
    d.text((px + 16, 124), "16-bit tag", font=f(SANS_B, 16), fill=GREEN_D)
    for i, t in enumerate([
        "space  = 2^16 = 65,536 values",
        "birthday bound = 321 messages",
        "brute force    = 65,536 messages",
    ]):
        d.text((px + 16, 156 + i * 24), t, font=fm, fill=INK)

    d.rounded_rectangle([px, 254, 1146, 380], radius=8, fill=(255, 249, 219),
                        outline=AMBER, width=2)
    d.text((px + 16, 268), "256-bit tag", font=f(SANS_B, 16), fill=(140, 105, 10))
    for i, t in enumerate([
        "space  = 2^256 = 1.16e77 values",
        "birthday bound = 2^128 messages",
        "unreachable: 1e22 years at 1e9/s",
    ]):
        d.text((px + 16, 300 + i * 24), t, font=fm, fill=INK)

    d.rounded_rectangle([34, 490, 1146, 542], radius=6, fill=(252, 240, 240),
                        outline=(170, 60, 60), width=1)
    d.text((50, 508), "Same generator, 10 bits removed from the tag: the attack goes "
                      "from 2^128 work to 321 messages.", font=fm, fill=(120, 40, 40))

    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


def render_stretching_diagram(rows, out_name="diagram_stretching.png"):
    """rows = [(iterations, best_ms), ...]"""
    W, H = 1180, 470
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fm = f(MONO, 14)

    d.text((34, 22), "Hash stretching: cost grows linearly with the iteration count",
           font=f(SANS_B, 23), fill=GREEN_D)
    d.text((34, 58), "PBKDF2-HMAC-SHA256, 32-byte derived key, measured on this machine "
                     "- log scale", font=fm, fill=GREY)

    # bars (log scale on y)
    x0, y0, x1, y1 = 100, 110, 620, 400
    lo, hi = 0.3, 200.0
    d.line([x0, y0, x0, y1], fill=(150, 150, 150))
    d.line([x0, y1, x1, y1], fill=(150, 150, 150))
    for v, lab in [(0.5, "0.5"), (1, "1"), (10, "10"), (100, "100")]:
        yy = y1 - (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (y1 - y0)
        d.line([x0, yy, x1, yy], fill=(232, 234, 230))
        d.text((x0 - 44, yy - 7), lab, font=fm, fill=GREY)
    d.text((34, 84), "time (ms)", font=fm, fill=GREY)

    bw, gap = 110, 70
    for i, (it, ms) in enumerate(rows):
        bx = x0 + 50 + i * (bw + gap)
        frac = (math.log10(ms) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
        bh = max(4, frac * (y1 - y0))
        d.rectangle([bx, y1 - bh, bx + bw, y1], fill=(232, 245, 233),
                    outline=GREEN_M, width=2)
        d.text((bx + bw / 2, y1 - bh - 22), f"{ms:.1f}", font=f(SANS_B, 15),
               fill=GREEN_D, anchor="mm")
        d.text((bx + bw / 2, y1 + 14), f"{it:,}", font=fm, fill=INK, anchor="mm")
    d.text(((x0 + x1) / 2, y1 + 42), "iterations", font=fm, fill=INK, anchor="mm")

    # right panel: attacker cost
    px = 670
    d.rounded_rectangle([px, 110, 1146, 400], radius=8, fill=(235, 241, 250),
                        outline=NAVY, width=2)
    d.text((px + 18, 124), "Attacker cost per guess", font=f(SANS_B, 16), fill=NAVY)
    d.text((px + 18, 150), "GPU: 1e10 SHA-256 ops/s  -  bars on log scale",
           font=fm, fill=GREY)
    for i, (it, ms) in enumerate(rows):
        y = 182 + i * 62
        gps = 1e10 / it
        d.text((px + 18, y), f"{it:>7,} iterations", font=fm, fill=INK)
        d.text((px + 18, y + 22), f"{gps:,.0f} guesses/s", font=fm, fill=(30, 80, 160))
        # bar
        bar_w = 300 * (math.log10(gps) / 11)
        d.rectangle([px + 250, y + 2, px + 250 + bar_w, y + 16],
                    fill=(150, 180, 220))
    d.text((px + 18, 372), "100,000x slower than one plain SHA-256", font=fm, fill=NAVY)

    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


def render_salt_diagram(out_name="diagram_salt.png"):
    W, H = 1180, 400
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fm = f(MONO, 14)

    d.text((34, 22), "Same password, different salt, different stored hash",
           font=f(SANS_B, 23), fill=GREEN_D)
    d.text((34, 58), "the salt is stored next to the hash - it is not secret, it only "
                     "has to be unique per user", font=fm, fill=GREY)

    def record(y, user, salt, h, colour):
        d.text((34, y + 26), user, font=f(SANS_B, 16), fill=colour)
        d.rounded_rectangle([150, y, 430, y + 64], radius=6, fill=(232, 245, 233),
                            outline=colour, width=2)
        d.text((166, y + 12), "password", font=fm, fill=GREY)
        d.text((166, y + 36), "HashLab@2026", font=fm, fill=INK)
        d.rounded_rectangle([446, y, 726, y + 64], radius=6, fill=(255, 249, 219),
                            outline=AMBER, width=2)
        d.text((462, y + 12), "salt (random)", font=fm, fill=GREY)
        d.text((462, y + 36), salt, font=fm, fill=INK)
        d.rounded_rectangle([742, y, 1146, y + 64], radius=6, fill=(235, 241, 250),
                            outline=NAVY, width=2)
        d.text((758, y + 12), "stored hash", font=fm, fill=GREY)
        d.text((758, y + 36), h, font=fm, fill=INK)

    record(110, "User A", "7bb39e51...03bb011e", "795f3c80...4313df9a4", GREEN_D)
    record(200, "User B", "af54691c...064a88cf", "fc940e7e...3a2a87f0e", GREEN_M)

    d.rounded_rectangle([34, 300, 1146, 372], radius=6, fill=(252, 240, 240),
                        outline=(170, 60, 60), width=1)
    d.text((50, 312), "Unsalted: one rainbow table cracks every account that shares the "
                      "password.", font=fm, fill=(120, 40, 40))
    d.text((50, 340), "Salted: the attacker must rebuild the table for each of the 2^128 "
                      "possible salts.", font=fm, fill=(120, 40, 40))

    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


# ----------------------------------------------------------------------
def parse_task1():
    txt = open(os.path.join(HERE, "out1.txt"), encoding="utf-8").read()
    n = int(re.search(r"Messages generated : (\d+)", txt).group(1))
    p = float(re.search(r"Collision probability : ([\d.]+)%", txt).group(1))
    return n, p


def parse_task3():
    txt = open(os.path.join(HERE, "out3.txt"), encoding="utf-8").read()
    rows = []
    for m in re.finditer(r"^\s*([\d,]+)\s+([\d.]+)\s+[\d.]+\s+[\d.]+\s+[\d.]+x\s*$",
                         txt, re.M):
        rows.append((int(m.group(1).replace(",", "")), float(m.group(2))))
    return rows


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)

    for name, title, out in [
        ("out1.txt", "task1_birthday_attack.py  -  16-bit birthday attack", "shot_task1.png"),
        ("out2.txt", "task2_sha256_collision.py  -  full SHA-256 scan", "shot_task2.png"),
        ("out3.txt", "task3_pbkdf2_stretching.py  -  PBKDF2 timing", "shot_task3.png"),
        ("out4.txt", "task4_password_salt.py  -  salted password store", "shot_task4.png"),
    ]:
        with open(os.path.join(HERE, name), encoding="utf-8") as fh:
            render_terminal(fh.read(), title, out)

    n, p = parse_task1()
    render_birthday_diagram(n, p)
    render_stretching_diagram(parse_task3())
    render_salt_diagram()
