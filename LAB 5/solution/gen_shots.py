#!/usr/bin/env python3
"""Render terminal-style screenshots and diagrams with Pillow."""

import os
import re
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")
MONO = "/home/honeypot/.local/share/fonts/JetBrains/JetBrainsMonoNerdFont-Regular.ttf"
MONO_B = "/usr/share/fonts/liberation/LiberationMono-Bold.ttf"
SANS = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

BG = (30, 32, 36)
BAR = (44, 47, 52)
FG = (220, 223, 228)
DIM = (120, 126, 134)
GREEN = (126, 211, 122)
CYAN = (110, 200, 220)
YELLOW = (230, 200, 120)
RED = (235, 120, 120)
MAGENTA = (200, 150, 230)
WHITE = (245, 246, 248)


def f(path, size):
    return ImageFont.truetype(path, size)


def line_color(line):
    s = line.strip()
    if s.startswith("===="):
        return DIM
    if s.startswith("TASK"):
        return GREEN
    if "-> match: True" in s or "Round-trip OK  : True" in s or "Files identical : True" in s:
        return GREEN
    if "False" in s:
        return RED
    if re.match(r"^[A-Za-z0-9 ()./\-]{3,22}\s*:", s):
        return None          # label line, handled per-span
    if s.startswith("$"):
        return GREEN
    return FG


def wrap_line(line, fnt, avail):
    """Hard-wrap a long terminal line, indenting continuation lines."""
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


def render_terminal(text, title, out_name, width=1180, font_size=17, pad=26):
    fnt = f(MONO, font_size)
    fnt_b = f(MONO_B, font_size)
    avail = width - 2 * pad
    raw = text.rstrip("\n").split("\n")
    lines = []
    for ln in raw:
        lines.extend(wrap_line(ln, fnt, avail))

    lh = int(font_size * 1.52)
    cw = fnt.getlength("M")
    bar_h = 46
    h = bar_h + pad * 2 + lh * len(lines)

    img = Image.new("RGB", (width, h), BG)
    d = ImageDraw.Draw(img)

    # title bar
    d.rectangle([0, 0, width, bar_h], fill=BAR)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 22 + i * 22
        d.ellipse([cx - 7, bar_h // 2 - 7, cx + 7, bar_h // 2 + 7], fill=col)
    d.text((width // 2, bar_h // 2), title, font=f(MONO, 14),
           fill=(170, 175, 182), anchor="mm")

    y = bar_h + pad
    for line in lines:
        col = line_color(line)
        if col is not None:
            d.text((pad, y), line, font=fnt_b if line.strip().startswith("TASK") else fnt, fill=col)
        else:
            # split "label : value" and colour the two halves
            m = re.match(r"^(\s*)([^:]{1,40}?)(\s*:\s*)(.*)$", line)
            if m:
                ind, label, sep, val = m.groups()
                x = pad
                d.text((x, y), ind + label + sep, font=fnt, fill=CYAN)
                x += fnt.getlength(ind + label + sep)
                vc = GREEN if val.strip() in ("True",) else WHITE
                d.text((x, y), val, font=fnt, fill=vc)
            else:
                d.text((pad, y), line, font=fnt, fill=FG)
        y += lh

    # thin outer border
    d.rectangle([0, 0, width - 1, h - 1], outline=(58, 62, 68))
    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


def render_mitm_diagram(out_name="diagram_mitm.png"):
    W, H = 1180, 620
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fb = f(SANS_B, 22)
    fs = f(SANS, 16)
    fm = f(MONO, 15)

    d.text((30, 24), "Meet-in-the-Middle against Double DES", font=f(SANS_B, 26), fill=(27, 94, 32))
    d.text((30, 62), "C = E(k2, E(k1, P))   ->   the intermediate value is the meeting point",
           font=fm, fill=(90, 90, 90))

    # boxes
    def box(x, y, w, h, label, sub, fill, border):
        d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill, outline=border, width=2)
        d.text((x + w // 2, y + h // 2 - 12), label, font=fb, fill=border, anchor="mm")
        d.text((x + w // 2, y + h // 2 + 14), sub, font=fm, fill=(70, 70, 70), anchor="mm")

    def arrow(x1, y1, x2, y2, col=(60, 60, 60)):
        d.line([x1, y1, x2, y2], fill=col, width=3)
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        for s in (0.4, -0.4):
            d.line([x2, y2, x2 - 12 * math.cos(a - s), y2 - 12 * math.sin(a - s)], fill=col, width=3)

    # forward chain (top)
    y1 = 150
    box(40, y1, 130, 70, "P", "plaintext", (232, 245, 233), (27, 94, 32))
    box(240, y1, 170, 70, "E(k1, .)", "guess k1", (232, 245, 233), (46, 125, 50))
    box(480, y1, 170, 70, "X", "intermediate", (255, 249, 219), (180, 140, 20))
    box(720, y1, 170, 70, "E(k2, .)", "guess k2", (232, 245, 233), (46, 125, 50))
    box(960, y1, 150, 70, "C", "ciphertext", (232, 245, 233), (27, 94, 32))

    arrow(172, y1 + 35, 238, y1 + 35)
    arrow(412, y1 + 35, 478, y1 + 35)
    arrow(652, y1 + 35, 718, y1 + 35)
    arrow(892, y1 + 35, 958, y1 + 35)

    # table
    d.rounded_rectangle([240, 290, 700, 430], radius=10, fill=(235, 241, 250), outline=(30, 80, 160), width=2)
    d.text((470, 312), "FORWARD TABLE", font=f(SANS_B, 17), fill=(30, 80, 160), anchor="mm")
    d.text((470, 348), "{ E(k1, P)  :  k1 }", font=fm, fill=(40, 40, 40), anchor="mm")
    d.text((470, 380), "2^k encryptions, 2^k memory", font=fm, fill=(90, 90, 90), anchor="mm")
    d.text((470, 408), "built once, then probed", font=fm, fill=(90, 90, 90), anchor="mm")
    arrow(325, 222, 325, 288, (30, 80, 160))

    # backward
    d.text((760, 300), "BACKWARD PHASE", font=f(SANS_B, 17), fill=(30, 80, 160))
    d.text((760, 332), "for each guess k2:", font=fm, fill=(40, 40, 40))
    d.text((760, 358), "  X' = D(k2, C)", font=fm, fill=(40, 40, 40))
    d.text((760, 384), "  if X' in table ->", font=fm, fill=(40, 40, 40))
    d.text((760, 410), "  keys found", font=fm, fill=(40, 40, 40))
    arrow(805, 222, 805, 296, (30, 80, 160))
    arrow(702, 360, 752, 360, (30, 80, 160))

    # bottom note
    d.rounded_rectangle([60, 470, 1120, 580], radius=8, fill=(252, 240, 240), outline=(170, 60, 60), width=2)
    d.text((80, 484), "Cost comparison", font=f(SANS_B, 17), fill=(150, 40, 40))
    d.text((80, 514), "brute force 2DES : 2^k * 2^k = 2^(2k) attempts",
           font=fm, fill=(60, 60, 60))
    d.text((80, 542), "MITM             : 2^k + 2^k = 2^(k+1) attempts  ->  only 2x harder than single DES",
           font=fm, fill=(60, 60, 60))

    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


def render_container_diagram(out_name="diagram_container.png"):
    W, H = 1180, 330
    img = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(img)
    fm = f(MONO, 15)
    d.text((30, 24), "AES-CBC file container layout", font=f(SANS_B, 24), fill=(27, 94, 32))
    d.text((30, 60), "key is NOT stored in the file - it is kept by the caller",
           font=fm, fill=(90, 90, 90))

    y = 110
    blocks = [
        ("MAGIC", "8 B", "AESCBC01", (232, 245, 233), (27, 94, 32)),
        ("SIZE", "8 B", "original bytes", (232, 245, 233), (27, 94, 32)),
        ("IV", "16 B", "random, clear", (255, 249, 219), (180, 140, 20)),
        ("CIPHERTEXT", "n x 16 B", "chunks of 64 KB", (235, 241, 250), (30, 80, 160)),
    ]
    x = 60
    widths = [150, 210, 210, 420]
    for (name, size, sub, fill, border), w in zip(blocks, widths):
        d.rectangle([x, y, x + w, y + 96], fill=fill, outline=border, width=2)
        d.text((x + w // 2, y + 28), name, font=f(SANS_B, 16), fill=border, anchor="mm")
        d.text((x + w // 2, y + 54), size, font=fm, fill=(60, 60, 60), anchor="mm")
        d.text((x + w // 2, y + 78), sub, font=fm, fill=(90, 90, 90), anchor="mm")
        x += w

    d.text((60, 232), "total header = 32 bytes        payload = plaintext + 16 byte PKCS#7 pad block",
           font=fm, fill=(70, 70, 70))
    d.text((60, 262), "last block is padded exactly once at EOF; one block is held back during streaming",
           font=fm, fill=(70, 70, 70))
    d.text((60, 292), "decrypt: read header -> verify magic -> unpad final block -> compare size",
           font=fm, fill=(70, 70, 70))

    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))

    for name, title, out in [
        ("out1.txt", "task1_des.py  -  DES ECB", "shot_task1.png"),
        ("out2.txt", "task2_mitm.py  -  MITM attack", "shot_task2.png"),
        ("out3.txt", "task3_aes.py  -  AES CBC + file", "shot_task3.png"),
    ]:
        with open(os.path.join(here, name), encoding="utf-8") as fh:
            render_terminal(fh.read(), title, out)

    render_mitm_diagram()
    render_container_diagram()
