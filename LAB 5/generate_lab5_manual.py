#!/usr/bin/env python3
"""
Information Security Lab - Lab Manual 05 Generator
Author: Muhammad Fezan (Fall-23-BSCS-466)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Course: Information Security Lab (7th Semester - Fall 2026)
Topic: Block Ciphers - DES architecture, permutations, key transformation,
       S-boxes, AES-CBC implementation, file encryption, Meet-in-the-Middle.
"""

import os
from PIL import Image as PILImage

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Preformatted, Image as RLImage, KeepTogether
)

# === LGU BRAND COLORS ===
G  = HexColor("#1B5E20")
LG = HexColor("#E8F5E9")
AG = HexColor("#2E7D32")
TD = HexColor("#212121")
SG = HexColor("#555555")
FG = HexColor("#777777")
BG_CODE = HexColor("#F8F9FA")
BORDER_CODE = HexColor("#CFD8DC")
NAVY = HexColor("#1A237E")

PAGE_W, PAGE_H = A4
LM = RM = TM = BM = 1 * inch
CW = PAGE_W - LM - RM
SB_W = 12 * mm

LAB_DIR = "/home/honeypot/Univeristy_Data/IS(L)/LAB 5"
SOL_DIR = os.path.join(LAB_DIR, "solution")
SHOT_DIR = os.path.join(SOL_DIR, "shots")
LOGO_PATH = "/home/honeypot/.hermes/skills/lgu-assignment/assets/lgu-logo.png"
OUT_PDF = os.path.join(LAB_DIR, "Information_Security_Lab_Manual_05.pdf")


def S(name, font="Times-Roman", size=12, color=TD, align=TA_LEFT,
      bold=False, italic=False, sa=4, sb=0, li=0, leading=None):
    fname = "Times-Bold" if bold else ("Times-Italic" if italic else font)
    return ParagraphStyle(name, fontName=fname, fontSize=size, textColor=color,
                          alignment=align, spaceAfter=sa, spaceBefore=sb,
                          leading=leading or (size * 1.3), leftIndent=li)


s_ct = S("ct", size=10, color=G, align=TA_CENTER, bold=True, sa=3)
s_ctt = S("ctt", size=18, color=G, align=TA_CENTER, bold=True, sa=4)
s_cs = S("cs", size=10.5, color=SG, align=TA_CENTER, italic=True, sa=6)
s_cl = S("cl", size=10, color=G, bold=True)
s_cv = S("cv", size=10, color=TD)

s_h1 = S("h1", size=12.5, color=G, bold=True, sa=3, sb=1)
s_h2 = S("h2", size=9.8, color=AG, bold=True, sa=2, sb=5)
s_body = S("body", size=9, color=TD, sa=2.5, leading=12.5, align=TA_JUSTIFY)
s_bul = S("bul", size=9, color=TD, sa=1.5, leading=12.2, li=12)
s_callout = S("callout", size=8.6, color=TD, sa=0, leading=11.6)
s_cap = S("cap", size=8, color=SG, align=TA_CENTER, italic=True, sa=6, sb=2)
s_tb = S("tb", size=8.4, color=TD, sa=0, leading=10.6)
s_th = S("th", size=8.4, color=HexColor("#FFFFFF"), align=TA_CENTER, bold=True, sa=0)

code_style = ParagraphStyle("CodeStyle", fontName="Courier", fontSize=6.9,
                            leading=8.4, textColor=NAVY)


def draw_sidebar(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(G)
    canvas.rect(0, 0, SB_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


def on_first_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    canvas.setFillColor(FG)
    canvas.drawCentredString(PAGE_W / 2, 0.5 * inch,
                             "Lahore Garrison University  |  Department of Computer Science")
    canvas.restoreState()
    draw_sidebar(canvas, doc)


def on_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 8.5)
    canvas.setFillColor(FG)
    canvas.drawString(LM, PAGE_H - 0.6 * inch,
                      "Information Security Lab  |  Lab Manual 05  -  Block Ciphers: DES, AES & Meet-in-the-Middle")
    canvas.setStrokeColor(HexColor("#E0E0E0"))
    canvas.setLineWidth(0.5)
    canvas.line(LM, PAGE_H - 0.65 * inch, PAGE_W - RM, PAGE_H - 0.65 * inch)
    canvas.drawCentredString(PAGE_W / 2, 0.5 * inch,
                             f"Page {canvas.getPageNumber()}  |  M.Fezan  |  Fall-23-BSCS-466")
    canvas.restoreState()


def styled_img(path, max_w, max_h):
    if not os.path.exists(path):
        return Paragraph(f"[Image missing: {path}]", s_body)
    im = PILImage.open(path)
    pw, ph = im.size
    scale = min(max_w / pw, max_h / ph)
    w, h = pw * scale, ph * scale
    rl = RLImage(path, width=w, height=h)
    rl.hAlign = 'CENTER'
    tbl = Table([[rl]], colWidths=[w + 4])
    tbl.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor("#B0BEC5")),
        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#FAFAFA")),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    tbl.hAlign = 'CENTER'
    return tbl


def shot(name, caption, max_h=300):
    return [styled_img(os.path.join(SHOT_DIR, name), CW - 8, max_h),
            Paragraph(caption, s_cap)]


def make_callout(text, bg=LG, border=AG, title=None):
    paras = []
    if title:
        paras.append(Paragraph(f"<b>{title}</b>",
                               S("ctitle", size=9, color=border, bold=True, sa=2)))
    paras.append(Paragraph(text, s_callout))
    tbl = Table([[paras]], colWidths=[CW])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LINELEFT', (0, 0), (0, -1), 2.5, border),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor("#C8E6C9") if bg == LG else HexColor("#CFD8DC")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return tbl


def make_code_box(code_text):
    pre = Preformatted(code_text.strip("\n"), code_style)
    tbl = Table([[pre]], colWidths=[CW])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_CODE),
        ('LINELEFT', (0, 0), (0, -1), 2.5, G),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_CODE),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return tbl


def make_code_blocks(code_text, n_parts=2):
    """Split a long listing into n_parts near-equal boxes, breaking at blank lines."""
    lines = code_text.strip("\n").split("\n")
    total = len(lines)
    cuts, prev = [], 0
    for i in range(1, n_parts):
        target = round(total * i / n_parts)
        best, best_d = target, 99
        for d in range(0, 9):
            for cand in (target - d, target + d):
                if prev + 4 < cand < total - 4 and lines[cand - 1].strip() == "":
                    best, best_d = cand, d
                    break
            if best_d < 99:
                break
        cuts.append(best)
        prev = best
    parts, start = [], 0
    for c in cuts + [total]:
        parts.append("\n".join(lines[start:c]))
        start = c
    out = []
    for part in parts:
        out.append(make_code_box(part))
        out.append(Spacer(1, 3))
    return out


def make_table(headers, rows, widths):
    data = [[Paragraph(h, s_th) for h in headers]]
    for r in rows:
        data.append([Paragraph(c, s_tb) for c in r])
    tbl = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), G),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor("#A5D6A7")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        style.append(('BACKGROUND', (0, i), (-1, i), LG if i % 2 == 0 else HexColor("#FFFFFF")))
    tbl.setStyle(TableStyle(style))
    return tbl


def read_code(fname):
    with open(os.path.join(SOL_DIR, fname), encoding="utf-8") as f:
        return f.read()


def build_cover():
    main_w = CW - SB_W
    items = []
    try:
        logo = RLImage(LOGO_PATH, width=24 * mm, height=24 * mm)
        logo.hAlign = 'CENTER'
        items.append(logo)
    except Exception:
        items.append(Paragraph("<b>LAHORE GARRISON UNIVERSITY</b>",
                               S("lf", size=14, color=G, align=TA_CENTER, bold=True)))

    items.append(Spacer(1, 2 * mm))
    items.append(Paragraph("LAHORE GARRISON UNIVERSITY",
                           S("lgu_u", size=13, color=G, align=TA_CENTER, bold=True, sa=2)))
    items.append(Paragraph("Department of Computer Science",
                           S("lgu_d", size=9.5, color=SG, align=TA_CENTER, sa=3)))
    items.append(Spacer(1, 2 * mm))
    items.append(Paragraph("INFORMATION SECURITY LAB", s_ct))
    items.append(Paragraph("LAB MANUAL # 5", s_ctt))
    items.append(Paragraph("Block Ciphers: DES Architecture, Key Transformation, "
                           "S-Boxes, AES Implementation & Meet-in-the-Middle Attack", s_cs))
    items.append(Spacer(1, 2 * mm))
    items.append(HRFlowable(width="100%", thickness=1, color=AG, spaceAfter=4))
    items.append(Spacer(1, 2 * mm))

    info = [
        [Paragraph("<b>SUBMITTED TO:</b>", s_cl), Paragraph("Sir Mukkaram Ahmad (Asst. Lect.)", s_cv)],
        [Paragraph("<b>SUBMITTED BY:</b>", s_cl), Paragraph("M.Fezan", s_cv)],
        [Paragraph("<b>ROLL NUMBER:</b>", s_cl), Paragraph("Fall-23-BSCS-466", s_cv)],
        [Paragraph("<b>COURSE:</b>", s_cl), Paragraph("Information Security Lab", s_cv)],
        [Paragraph("<b>SECTION:</b>", s_cl), Paragraph("L", s_cv)],
        [Paragraph("<b>SEMESTER:</b>", s_cl), Paragraph("7th (Fall 2026)", s_cv)],
        [Paragraph("<b>CONTEXT:</b>", s_cl), Paragraph("Lab Manual # 5 - Week 06 (Block Ciphers)", s_cv)],
    ]
    it = Table(info, colWidths=[38 * mm, main_w - 38 * mm])
    it.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, HexColor("#EEEEEE")),
    ]))
    items.append(it)
    items.append(Spacer(1, 4 * mm))
    items.append(HRFlowable(width="100%", thickness=1, color=AG, spaceAfter=0))

    mn_tbl = Table([[p] for p in items], colWidths=[main_w])
    mn_tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    cover = Table([[Spacer(SB_W, 1), mn_tbl]], colWidths=[SB_W, main_w])
    cover.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return [cover, PageBreak()]


# ======================================================================
# CONTENT
# ======================================================================
def build():
    e = build_cover()

    # ---------------- Overview ----------------
    e.append(Paragraph("Lab 05 - Objectives and Scope", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "This lab covers the design and practical implementation of <b>block ciphers</b>. "
        "A block cipher takes a fixed-size block of plaintext (8 bytes for DES, 16 bytes for AES) and a key, "
        "and produces a block of ciphertext of the same size. The lab is divided into three tasks: "
        "DES encryption/decryption in ECB mode, a theoretical and practical treatment of the "
        "Meet-in-the-Middle attack on Double DES, and an AES-CBC implementation extended to streaming "
        "file encryption.", s_body))
    e.append(Spacer(1, 2))
    e.append(Paragraph("Learning outcomes (CLO 4 / C4):", s_h2))
    for t in [
        "Explain the internal architecture of DES: initial and final permutations, the 16-round Feistel network, "
        "the key schedule (PC-1, PC-2) and the eight S-boxes.",
        "Implement DES and AES with the <i>Crypto.Cipher</i> module and apply correct PKCS#7 padding.",
        "Implement AES in CBC mode with a random key and IV, and extend it to chunked file encryption.",
        "Analyse why Double DES fails against a Meet-in-the-Middle attack and quantify the loss of security.",
    ]:
        e.append(Paragraph(f"&bull; {t}", s_bul))
    e.append(Spacer(1, 3))

    e.append(make_callout(
        "<b>Environment used for every task:</b> Python 3.11 with <i>pycryptodome</i> 4.1.0 "
        "(package name <i>Crypto</i>), executed inside the Hermes virtual environment at "
        "/home/honeypot/.hermes/hermes-agent/venv. All screenshots in this manual are real program output, "
        "rendered with Pillow and embedded with ReportLab.", title="Tooling"))

    # ---------------- DES theory ----------------
    e.append(Paragraph("1. DES Internal Architecture", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "DES is a symmetric Feistel cipher operating on 64-bit blocks with a 64-bit key, of which only "
        "<b>56 bits are effective</b>: bit 8 of every key byte is a parity bit and is discarded by the key "
        "schedule. Encryption is a fixed sequence of stages.", s_body))
    e.append(Spacer(1, 2))

    e.append(make_table(
        ["#", "Operation", "Details"],
        [
            ["1", "Initial Permutation (IP)",
             "Reorders the 64 plaintext bits according to a fixed 8x8 table. It has no cryptographic "
             "value by itself; it exists only to make software and hardware implementations share a layout."],
            ["2", "16 Feistel rounds",
             "L(i) = R(i-1);  R(i) = L(i-1) XOR f(R(i-1), K(i)). Each round is invertible without needing "
             "a separate decryption circuit."],
            ["3", "Round function f",
             "Expansion E: 32 -> 48 bits, XOR with 48-bit subkey, then eight S-boxes map 6 bits to 4 bits "
             "(non-linear core), then P-permutation spreads the 32 output bits."],
            ["4", "Key transformation",
             "PC-1 drops parity bits and permutes 64 -> 56 bits into C and D halves. Each round rotates C and D "
             "left by 1 or 2 positions, and PC-2 selects 48 of the 56 bits as the round subkey."],
            ["5", "Swap halves",
             "After round 16 the two halves are swapped (R16 || L16) so encryption and decryption use the "
             "same code path with the subkey order reversed."],
            ["6", "Final Permutation (FP)",
             "The inverse of IP, producing the 64-bit ciphertext block."],
        ],
        [22, 108, CW - 130]))

    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "The <b>S-boxes</b> are the only non-linear component, and therefore the only part that provides "
        "confusion. Each S-box is a 4x16 lookup table: the outer two bits of the 6-bit input select the row, "
        "the inner four bits select the column. Without S-boxes the entire cipher would collapse into a "
        "linear (affine) function over GF(2) and would be breakable with linear algebra.", s_body))
    e.append(Spacer(1, 2))
    e.append(make_callout(
        "<b>ECB mode used in Task 1:</b> each 64-bit block is encrypted independently with the same key. "
        "This is deterministic, so identical plaintext blocks produce identical ciphertext blocks. ECB is "
        "used here only to demonstrate the raw cipher; it must never be used for real data because it leaks "
        "block-level structure. CBC (Task 3) fixes this by chaining blocks through an IV.",
        bg=HexColor("#FFF8E1"), border=HexColor("#B08800"), title="Mode note"))
    e.append(PageBreak())

    # ---------------- Task 1 ----------------
    e.append(Paragraph("Task 1 - DES Encryption and Decryption (ECB)", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "<b>Requirement:</b> implement DES with the <i>Crypto.Cipher</i> module in ECB mode, using a random "
        "8-byte key and PKCS#7 padding, and display the original data, the ciphertext bytes and the decrypted "
        "output.", s_body))
    e.append(Spacer(1, 3))
    e.append(Paragraph("Implementation (task1_des.py)", s_h2))
    e.append(make_code_box(read_code("task1_des.py")))
    e.append(Spacer(1, 4))
    e.append(KeepTogether([Paragraph("Execution output", s_h2)] +
                          shot("shot_task1.png",
                               "Fig. 1: DES-ECB run - 59-byte plaintext padded to 64 bytes, "
                               "8 blocks, exact round-trip recovery.", max_h=290)))
    e.append(Spacer(1, 3))

    e.append(Paragraph("Result analysis", s_h2))
    e.append(Paragraph(
        "The 59-byte plaintext does not fill an integer number of 8-byte blocks. PKCS#7 appends "
        "<i>8 - (59 mod 8) = 5</i> bytes, each with the value 0x05, so the padded length becomes 64 bytes and "
        "the ciphertext is exactly 8 blocks long. During decryption, <i>unpad()</i> reads the last byte (0x05), "
        "verifies that the last five bytes all equal 0x05, and strips them. Because the key is random on every "
        "run, the ciphertext is different each time, while the recovered plaintext is always identical.", s_body))
    e.append(Spacer(1, 3))
    e.append(make_table(
        ["Property", "Value observed"],
        [
            ["Key length", "8 bytes = 64 bits (56 effective bits after parity removal)"],
            ["Block size", "8 bytes = 64 bits"],
            ["Plaintext length", "59 bytes"],
            ["Padded length", "64 bytes (5 bytes of 0x05 padding added)"],
            ["Ciphertext length", "64 bytes = 8 blocks"],
            ["Round-trip result", "Decrypted plaintext is byte-identical to the original (True)"],
        ],
        [120, CW - 120]))
    # ---------------- Task 2 ----------------
    e.append(KeepTogether(
        [Paragraph("Task 2 - Meet-in-the-Middle Attack on Double DES", s_h1),
         HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4),
         Paragraph(
             "Double DES encrypts twice with two independent keys: <b>C = E(k2, E(k1, P))</b>. The naive "
             "assumption is that the key space becomes 2^56 x 2^56 = 2^112, which would be far beyond brute "
             "force. That assumption is false. The Meet-in-the-Middle attack does not search for the pair of "
             "keys simultaneously; it searches for the <b>intermediate value</b> from both ends and meets in "
             "the middle.", s_body),
         Spacer(1, 3)]
        + shot("diagram_mitm.png", "Fig. 2: The two phases of the attack meet at the intermediate "
                                   "value X = E(k1, P) = D(k2, C).", max_h=230)))
    e.append(Spacer(1, 2))

    e.append(Paragraph("2.1 Step-by-step workflow", s_h2))
    steps = [
        ("Step 1 - Known plaintext.", "The attacker needs at least one known plaintext/ciphertext pair (P, C) "
                                      "for the same key pair. In a known-plaintext attack this is realistic: file "
                                      "headers, protocol handshakes and fixed message fields are predictable."),
        ("Step 2 - Forward phase (plaintext side).", "For every candidate k1 in the 2^56 keyspace, compute "
                                                     "X = E(k1, P) and store the pair (X, k1) in a hash table keyed by X. "
                                                     "This costs 2^56 encryptions and 2^56 table entries."),
        ("Step 3 - Backward phase (ciphertext side).", "For every candidate k2 in the 2^56 keyspace, compute "
                                                       "X' = D(k2, C) and look X' up in the table."),
        ("Step 4 - The match.", "A hit means E(k1, P) = D(k2, C), which is exactly the condition "
                                "C = E(k2, E(k1, P)). The pair (k1, k2) is a candidate key pair."),
        ("Step 5 - Verification.", "A candidate pair must be confirmed on a second known plaintext/ciphertext "
                                   "pair, because random collisions can produce false positives. With a 64-bit block "
                                   "and 2^56 forward entries, the expected number of false candidates is about "
                                   "2^56 / 2^64 = 2^-8, so usually only the correct pair survives."),
        ("Step 6 - Total cost.", "2^56 + 2^56 = 2^57 encryptions, plus 2^56 memory. Double DES is therefore only "
                                 "<b>twice</b> as hard as single DES, not 2^56 times harder."),
    ]
    for title, text in steps:
        e.append(Paragraph(f"<b>{title}</b> {text}", s_bul))
    e.append(Spacer(1, 3))

    e.append(Paragraph("2.2 Assumptions", s_h2))
    for t in [
        "The attacker has at least one, preferably two, known plaintext/ciphertext pairs produced under the "
        "same key pair.",
        "The block cipher is deterministic and the same key is reused across messages (true for both DES and 2DES).",
        "The attacker has enough memory for 2^56 entries (roughly 2^59 bytes for 8-byte blocks plus key index). "
        "Memory, not time, is the practical bottleneck of the attack.",
        "The keys are independent. If k1 = k2 the scheme degenerates to single DES and the attack trivially succeeds.",
    ]:
        e.append(Paragraph(f"&bull; {t}", s_bul))
    e.append(Spacer(1, 3))

    cmp_table = make_table(
        ["Approach", "Time", "Memory", "Comment"],
        [
            ["Exhaustive search on 2DES", "2^112", "negligible", "Infeasible"],
            ["Meet-in-the-Middle on 2DES", "2^57", "2^56 entries", "Only 2x the cost of breaking single DES"],
            ["Single DES exhaustive search", "2^56", "negligible", "Already broken by dedicated hardware"],
        ],
        [130, 55, 70, CW - 255])
    e.append(KeepTogether([cmp_table]))
    e.append(Spacer(1, 3))
    e.append(make_callout(
        "This is the reason 2DES was never standardised and why 3DES uses three keys with a "
        "decrypt-encrypt-decrypt construction (EDE), which raises the MITM cost to about 2^112. "
        "The same argument is why AES-128 alone is preferred over any cascade of 56-bit ciphers.",
        bg=HexColor("#E3F2FD"), border=HexColor("#1A237E"), title="Why 2DES is not used"))
    e.append(Spacer(1, 4))

    e.append(Paragraph("2.3 Working demonstration (scaled keyspace)", s_h2))
    e.append(Paragraph(
        "A full 2^56 table cannot be built in a lab. The program below executes the <b>exact same algorithm</b> "
        "on a 14-bit keyspace, so the attack finishes in seconds while the complexity argument is unchanged. "
        "The keys are constructed with only 7 varying bits per key byte because DES discards the parity bit: if "
        "the counter were spread over parity positions, several counters would map to the same effective key and "
        "the recovered value would appear wrong even though the attack succeeded.", s_body))
    e.append(Spacer(1, 3))
    e.extend(make_code_blocks(read_code("task2_mitm.py"), 2))

    e.append(Paragraph("Attack output", s_h2))
    for f in shot("shot_task2.png", "Fig. 3: MITM run - both halves of the key recovered exactly, and the "
                                    "recovered pair reproduces the original ciphertext.", max_h=235):
        e.append(f)
    e.append(Spacer(1, 3))
    e.append(Paragraph(
        "The forward table holds 16,384 entries, one per candidate k1. The backward phase decrypts the "
        "ciphertext under each candidate k2 and probes the table; the first probe that hits returns the pair "
        "(0x0a2b, 0x1c4d), which is exactly the secret key pair. Re-encrypting the plaintext with the recovered "
        "keys reproduces the ciphertext byte for byte, so the attack is verified, not merely plausible. The "
        "measured work was 32,768 block operations against 268,435,456 for exhaustive search on the same "
        "keyspace, an 8,192x reduction that matches the theoretical 2^(2k) / 2^(k+1) = 2^(k-1) factor.", s_body))
    e.append(Spacer(1, 4))

    # ---------------- Task 3 ----------------
    e.append(Paragraph("Task 3 - AES in CBC Mode and File Encryption", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "AES is a substitution-permutation network over a 16-byte state. It replaces the Feistel structure of "
        "DES with four invertible transformations applied per round: <b>SubBytes</b> (non-linear byte "
        "substitution using the GF(2^8) inverse), <b>ShiftRows</b> (diffusion across columns), "
        "<b>MixColumns</b> (matrix multiplication in GF(2^8)) and <b>AddRoundKey</b>. AES-128 uses 10 rounds "
        "with an 11th subkey derived from the 16-byte key by the Rijndael key expansion.", s_body))
    e.append(Spacer(1, 2))
    e.append(Paragraph(
        "In <b>CBC mode</b> every plaintext block is XORed with the previous ciphertext block before "
        "encryption, so identical plaintext blocks no longer produce identical ciphertext. The first block is "
        "XORed with the <b>Initialization Vector</b>, which must be random and unpredictable but does not need "
        "to be secret, hence it is stored in clear next to the ciphertext.", s_body))
    e.append(Spacer(1, 3))

    e.append(Paragraph("3.1 Text encryption (task3_aes.py, part 1)", s_h2))
    e.append(make_code_box("""from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

BLOCK = AES.block_size                      # 16 bytes

def aes_encrypt_text(key, iv, text):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(text, BLOCK))

def aes_decrypt_text(key, iv, data):
    return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(data), BLOCK)

key = get_random_bytes(16)                  # 128-bit key
iv  = get_random_bytes(BLOCK)               # 128-bit IV
ct  = aes_encrypt_text(key, iv, msg)
pt  = aes_decrypt_text(key, iv, ct)         # must equal msg"""))
    e.append(Spacer(1, 4))

    e.append(Paragraph("3.2 Streaming file encryption", s_h2))
    e.append(Paragraph(
        "Encrypting a whole file in memory does not scale. The implementation reads the file in 64 KB chunks, "
        "which are already multiples of the 16-byte block, and keeps <b>one block of plaintext held back</b> at "
        "all times. That single block is the only one that ever receives PKCS#7 padding, so padding is applied "
        "exactly once, at end of file, instead of after every chunk. The same hold-back logic runs in reverse "
        "during decryption, so only the final block is unpadded.", s_body))
    e.append(Spacer(1, 2))
    for f in shot("diagram_container.png", "Fig. 4: Container layout - the original size is stored so the "
                                           "restored file can be validated after unpadding.", max_h=170):
        e.append(f)
    e.append(Spacer(1, 2))
    e.append(make_table(
        ["Field", "Size", "Purpose"],
        [
            ["MAGIC", "8 bytes", "Format tag 'AESCBC01'. Rejects files that are not this container."],
            ["SIZE", "8 bytes", "Original file length, big-endian. Used to verify the restored output."],
            ["IV", "16 bytes", "Random per file, stored in clear. Required to decrypt the first block."],
            ["CIPHERTEXT", "n x 16 bytes", "Encrypted chunks. The session key is never stored in the file."],
        ],
        [70, 65, CW - 135]))
    e.append(PageBreak())

    e.append(Paragraph("Implementation (task3_aes.py)", s_h2))
    e.extend(make_code_blocks(read_code("task3_aes.py"), 2))
    e.append(PageBreak())

    e.append(KeepTogether([Paragraph("Execution output", s_h2)] +
                          shot("shot_task3.png",
                               "Fig. 5: AES-CBC text round-trip and 300 KB file round-trip verified by SHA-256.",
                               max_h=320)))
    e.append(Spacer(1, 3))

    e.append(Paragraph("Result analysis", s_h2))
    e.append(Paragraph(
        "The 63-byte text message is padded to 64 bytes, giving four 16-byte blocks. The 300,000-byte file is "
        "already a multiple of 16, so PKCS#7 adds a complete block of 16 bytes (0x10 repeated), which is why the "
        "container holds 300,048 bytes: 32 bytes of header plus 300,016 bytes of ciphertext. A full padding block "
        "is correct behaviour and is what makes unpadding unambiguous: without it, a plaintext ending in 0x01 "
        "could not be distinguished from a padded one.", s_body))
    e.append(Spacer(1, 2))
    e.append(Paragraph(
        "The two SHA-256 digests are identical, so the restored file is bit-exact, and the stored size check "
        "confirms the unpadding removed exactly 16 bytes. The key is returned to the caller and never written to "
        "the container, so possession of the file alone is not enough to decrypt it.", s_body))
    e.append(Spacer(1, 4))
    e.append(make_table(
        ["Metric", "Text (3.1)", "File (3.2)"],
        [
            ["Input size", "63 bytes", "300,000 bytes"],
            ["Ciphertext size", "64 bytes", "300,016 bytes"],
            ["Blocks", "4", "18,751"],
            ["Padding added", "1 byte (0x01)", "16 bytes (0x10 block)"],
            ["Round-trip verified", "Direct byte comparison", "SHA-256 of source and restored file"],
            ["Result", "Identical", "Identical"],
        ],
        [105, 150, CW - 255]))
    e.append(Spacer(1, 5))

    # ---------------- Conclusion ----------------
    e.append(Paragraph("Conclusion", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "The three tasks show that the strength of a block cipher is not decided by the cipher alone. DES works "
        "correctly as a primitive: the padding, the key schedule and the Feistel structure all behave as "
        "specified, and the round-trip is exact. Its weakness is the 56-bit key. Cascading two DES instances "
        "does not repair that weakness, because the Meet-in-the-Middle attack turns a 2^112 search into a 2^57 "
        "search by trading memory for time, which the working demonstration reproduces exactly on a scaled "
        "keyspace. AES avoids the problem by using a 128-bit block and a 128-bit key, and CBC mode removes the "
        "determinism of ECB so that equal plaintext blocks produce different ciphertext. The file encryption task "
        "then shows the engineering side: correct streaming, one padding operation per file, the IV stored "
        "alongside the data, and the key kept out of the container.", s_body))
    e.append(Spacer(1, 4))

    e.append(Paragraph("References", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    for i, r in enumerate([
        "NIST FIPS 46-3, <i>Data Encryption Standard (DES)</i>, National Institute of Standards and Technology.",
        "NIST FIPS 197, <i>Advanced Encryption Standard (AES)</i>, November 2001.",
        "W. Stallings, <i>Cryptography and Network Security: Principles and Practice</i>, 7th ed., Pearson.",
        "A. J. Menezes, P. C. van Oorschot, S. A. Vanstone, <i>Handbook of Applied Cryptography</i>, CRC Press, "
        "Section 7.2 (Meet-in-the-middle attack).",
        "PyCryptodome documentation, <i>Crypto.Cipher.DES</i> and <i>Crypto.Cipher.AES</i>, "
        "https://pycryptodome.readthedocs.io",
    ], 1):
        e.append(Paragraph(f"[{i}] {r}", S(f"ref{i}", size=8.6, color=TD, sa=2, leading=11, li=16)))

    doc = SimpleDocTemplate(OUT_PDF, pagesize=A4, leftMargin=LM, rightMargin=RM,
                            topMargin=TM, bottomMargin=BM,
                            title="Information Security Lab Manual 05 - Block Ciphers",
                            author="M.Fezan (Fall-23-BSCS-466)")
    doc.build(e, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print("DONE:", OUT_PDF)


if __name__ == "__main__":
    build()
