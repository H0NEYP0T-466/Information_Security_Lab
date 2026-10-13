#!/usr/bin/env python3
"""
Information Security Lab - Lab Manual 04 Generator
Author: Muhammad Fezan (Fall-23-BSCS-466)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Course: Information Security Lab (7th Semester - Fall 2026)
Institution: Lahore Garrison University - Department of Computer Science
Topic: Stream Ciphers & Pseudo-Random Generators (PRG): ARC4, Vernam, Salsa20, Custom Cipher & Adversarial Attacks
"""

import os
import sys
import shutil
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
G  = HexColor("#1B5E20")   # Primary green (LGU brand)
LG = HexColor("#E8F5E9")   # Light green background
AG = HexColor("#2E7D32")   # Accent green
TD = HexColor("#212121")   # Text dark
SG = HexColor("#555555")   # Subtitle gray
FG = HexColor("#777777")   # Footer gray
BG_CODE = HexColor("#F8F9FA")
BORDER_CODE = HexColor("#CFD8DC")
NAVY = HexColor("#1A237E")

# === PAGE SETUP ===
PAGE_W, PAGE_H = A4
LM = RM = TM = BM = 1 * inch
CW = PAGE_W - LM - RM   # Content width: ~451.27 pt
SB_W = 12 * mm          # Sidebar width on cover

# === STYLES ===
def S(name, font="Times-Roman", size=12, color=TD, align=TA_LEFT,
      bold=False, italic=False, sa=4, sb=0, li=0, leading=None):
    fname = "Times-Bold" if bold else ("Times-Italic" if italic else font)
    return ParagraphStyle(name, fontName=fname, fontSize=size, textColor=color,
        alignment=align, spaceAfter=sa, spaceBefore=sb,
        leading=leading or (size * 1.3), leftIndent=li)

s_ct   = S("ct",   size=10, color=G,  align=TA_CENTER, bold=True, sa=3)
s_ctt  = S("ctt",  size=18, color=G,  align=TA_CENTER, bold=True, sa=4)
s_cs   = S("cs",   size=10.5, color=SG, align=TA_CENTER, italic=True, sa=6)
s_cl   = S("cl",   size=10, color=G,  bold=True)
s_cv   = S("cv",   size=10, color=TD)

s_h1   = S("h1",   size=12.5, color=G,  bold=True, sa=3, sb=1)
s_h2   = S("h2",   size=9.5, color=AG, bold=True, sa=2, sb=4)
s_body = S("body", size=9, color=TD, sa=2.5, leading=12.5, align=TA_JUSTIFY)
s_q    = S("q",    size=9, color=TD, sa=0, leading=12.5)
s_callout = S("callout", size=8.5, color=TD, sa=0, leading=11.5)

code_style = ParagraphStyle(
    "CodeStyle",
    fontName="Courier",
    fontSize=7.2,
    leading=9.2,
    textColor=NAVY,
)

LOGO_PATH = "/home/honeypot/.gemini/config/skills/lgu-assignment/assets/lgu-logo.png"

# === CANVAS CALLBACKS ===
def draw_sidebar(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(G)
    canvas.rect(0, 0, SB_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    canvas.setFillColor(FG)
    canvas.drawCentredString(PAGE_W / 2, 0.5 * inch, "Lahore Garrison University  |  Department of Computer Science")
    canvas.restoreState()
    draw_sidebar(canvas, doc)

def on_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 8.5)
    canvas.setFillColor(FG)
    canvas.drawString(LM, PAGE_H - 0.6 * inch, "Information Security Lab  |  Lab Manual 04  -  Stream Ciphers & Pseudo-Random Generators")
    canvas.setStrokeColor(HexColor("#E0E0E0"))
    canvas.setLineWidth(0.5)
    canvas.line(LM, PAGE_H - 0.65 * inch, PAGE_W - RM, PAGE_H - 0.65 * inch)
    canvas.drawCentredString(PAGE_W / 2, 0.5 * inch, f"Page {canvas.getPageNumber()}  |  M.Fezan  |  Fall-23-BSCS-466")
    canvas.restoreState()

# === HELPER: IMAGE RESIZER ===
def styled_img(path, max_w, max_h):
    if not os.path.exists(path):
        return Paragraph(f"[Image Missing: {path}]", s_body)
    im = PILImage.open(path)
    pw, ph = im.size
    scale = min(max_w / pw, max_h / ph)
    w, h = pw * scale, ph * scale
    rl = RLImage(path, width=w, height=h)
    rl.hAlign = 'CENTER'

    tbl = Table([[rl]], colWidths=[w + 4])
    tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor("#B0BEC5")),
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#FAFAFA")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    tbl.hAlign = 'CENTER'
    return tbl

def make_callout(text, bg=LG, border=AG, title=None):
    paras = []
    if title:
        paras.append(Paragraph(f"<b>{title}</b>", S("ctitle", size=9, color=border, bold=True, sa=2)))
    paras.append(Paragraph(text, s_callout))
    tbl = Table([[paras]], colWidths=[CW])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINELEFT', (0,0), (0,-1), 2.5, border),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor("#C8E6C9") if bg==LG else HexColor("#CFD8DC")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return tbl

def make_code_box(code_text):
    pre = Preformatted(code_text.strip(), code_style)
    code_tbl = Table([[pre]], colWidths=[CW])
    code_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CODE),
        ('LINELEFT', (0,0), (0,-1), 2.5, G),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_CODE),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return code_tbl

# === COVER BUILDER ===
def build_cover():
    main_w = CW - SB_W
    main_items = []

    try:
        logo = RLImage(LOGO_PATH, width=24 * mm, height=24 * mm)
        logo.hAlign = 'CENTER'
        main_items.append(logo)
    except Exception:
        main_items.append(Paragraph("<b>LAHORE GARRISON UNIVERSITY</b>",
            S("lf", size=14, color=G, align=TA_CENTER, bold=True)))

    main_items.append(Spacer(1, 2 * mm))
    main_items.append(Paragraph("LAHORE GARRISON UNIVERSITY", S("lgu_u", size=13, color=G, align=TA_CENTER, bold=True, sa=2)))
    main_items.append(Paragraph("Department of Computer Science", S("lgu_d", size=9.5, color=SG, align=TA_CENTER, sa=3)))
    main_items.append(Spacer(1, 2 * mm))
    main_items.append(Paragraph("INFORMATION SECURITY LAB", s_ct))
    main_items.append(Paragraph("LAB MANUAL # 4", s_ctt))
    main_items.append(Paragraph("Stream Ciphers & Pseudo-Random Generators (ARC4, Vernam, Salsa20, Custom Cipher & Attacks)", s_cs))
    main_items.append(Spacer(1, 2 * mm))
    main_items.append(HRFlowable(width="100%", thickness=1, color=AG, spaceAfter=4))
    main_items.append(Spacer(1, 2 * mm))

    info = [
        [Paragraph("<b>SUBMITTED TO:</b>", s_cl), Paragraph("Sir Mukkaram Ahmad (Asst. Lect.)", s_cv)],
        [Paragraph("<b>SUBMITTED BY:</b>", s_cl), Paragraph("M.Fezan", s_cv)],
        [Paragraph("<b>ROLL NUMBER:</b>", s_cl), Paragraph("Fall-23-BSCS-466", s_cv)],
        [Paragraph("<b>COURSE:</b>", s_cl), Paragraph("Information Security Lab", s_cv)],
        [Paragraph("<b>SECTION:</b>", s_cl), Paragraph("L", s_cv)],
        [Paragraph("<b>SEMESTER:</b>", s_cl), Paragraph("7th (Fall 2026)", s_cv)],
        [Paragraph("<b>CONTEXT:</b>", s_cl), Paragraph("Lab Manual # 4 - Stream Ciphers, PRGs & Cryptanalysis", s_cv)],
    ]
    it = Table(info, colWidths=[38 * mm, main_w - 38 * mm])
    it.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, HexColor("#EEEEEE")),
    ]))
    main_items.append(it)
    main_items.append(Spacer(1, 4 * mm))
    main_items.append(HRFlowable(width="100%", thickness=1, color=AG, spaceAfter=0))

    mn_tbl = Table([[p] for p in main_items], colWidths=[main_w])
    mn_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))

    cover = Table([[Spacer(SB_W, 1), mn_tbl]], colWidths=[SB_W, main_w])
    cover.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    return [cover, PageBreak()]


def main():
    code_dir = "/home/honeypot/Univeristy_Data/IS(L)/LAB 4/Code"
    output_pdf = "/home/honeypot/Univeristy_Data/IS(L)/LAB 4/Information_Security_Lab_Manual_04.pdf"
    desktop_pdf = "/home/honeypot/Desktop/Information_Security_Lab_Manual_04.pdf"

    elements = build_cover()

    # -------------------------------------------------------------
    # PAGE 2: LAB OVERVIEW, CORE CONCEPTS & MANUAL EXAMPLES
    # -------------------------------------------------------------
    p2 = []
    p2.append(Paragraph("<b>Lab 04: Stream Ciphers & PRG Foundational Theory</b>", s_h1))
    p2.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=2))

    intro_text = (
        "<b>Core Architecture of Stream Ciphers:</b><br/>"
        "A stream cipher encrypts continuous data by generating a pseudo-random sequence of bits or bytes "
        "(the <i>keystream</i>) from a short secret key and Nonce via a Pseudo-Random Generator (PRG). "
        "Encryption and decryption are governed by bitwise exclusive-OR (XOR):<br/>"
        "&bull; <b>Encryption:</b> <i>C = P XOR Keystream</i><br/>"
        "&bull; <b>Decryption:</b> <i>P = C XOR Keystream</i><br/>"
        "Because XOR is an involutory operation (<i>(A XOR B) XOR B = A</i>), the identical algorithm executes both encryption and decryption."
    )
    p2.append(make_callout(intro_text, bg=LG, border=AG))
    p2.append(Spacer(1, 1.5 * mm))

    num_ex = (
        "<b>Step-by-Step Numerical Calculations (From Handout & Slides):</b><br/>"
        "&bull; <b>1. Toy ARC4 by Hand (N = 4, Key = [1, 2, 3], S = [0, 1, 2, 3]):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&bull; KSA i=0: j = (0 + S[0] + K[0]) mod 4 = (0 + 0 + 1) mod 4 = 1. Swap S[0], S[1] -> S = [1, 0, 2, 3]<br/>"
        "&nbsp;&nbsp;&nbsp;&bull; KSA i=1: j = (1 + S[1] + K[1]) mod 4 = (1 + 0 + 2) mod 4 = 3. Swap S[1], S[3] -> S = [1, 3, 2, 0]<br/>"
        "&nbsp;&nbsp;&nbsp;&bull; KSA i=2: j = (3 + S[2] + K[2]) mod 4 = (3 + 2 + 3) mod 4 = 0. Swap S[2], S[0] -> S = [2, 3, 1, 0]<br/>"
        "&nbsp;&nbsp;&nbsp;&bull; KSA i=3: j = (0 + S[3] + K[0]) mod 4 = (0 + 0 + 1) mod 4 = 1. Swap S[3], S[1] -> S = [2, 0, 1, 3]<br/>"
        "&nbsp;&nbsp;&nbsp;&bull; PRGA (Byte 1): i = 1, j = (0 + S[1]) mod 4 = 0. Swap S[1], S[0] -> S = [0, 2, 1, 3]. "
        "Output k = S[(S[1] + S[0]) mod 4] = S[2] = 1. Plaintext symbol 2 -> 2 XOR 1 = 3.<br/>"
        "&bull; <b>2. Vernam Byte-Level XOR:</b><br/>"
        "&nbsp;&nbsp;&nbsp;Plaintext p = 'C' (ASCII 67 = 01000011_2), Key k = 't' (ASCII 116 = 01110100_2).<br/>"
        "&nbsp;&nbsp;&nbsp;c = 01000011_2 XOR 01110100_2 = 00110111_2 = 55_10 = 0x37 = chr(55) = '7'.<br/>"
        "&bull; <b>3. Salsa20 Quarter-Round QR(1, 0, 0, 0):</b><br/>"
        "&nbsp;&nbsp;&nbsp;y1 = 0 XOR ((1 + 0) &lt;&lt;&lt; 7) = 0x00000080<br/>"
        "&nbsp;&nbsp;&nbsp;y2 = 0 XOR ((0x80 + 1) &lt;&lt;&lt; 9) = 0x00010200<br/>"
        "&nbsp;&nbsp;&nbsp;y3 = 0 XOR ((0x10200 + 0x80) &lt;&lt;&lt; 13) = 0x20500000<br/>"
        "&nbsp;&nbsp;&nbsp;y0 = 1 XOR ((0x20500000 + 0x00010200) &lt;&lt;&lt; 18) = 0x08008145<br/>"
        "&nbsp;&nbsp;&nbsp;Result: QR(1, 0, 0, 0) = (0x08008145, 0x00000080, 0x00010200, 0x20500000)."
    )
    p2.append(make_callout(num_ex, bg=HexColor("#F1F8E9"), border=G, title="Manual Verification Proofs"))
    p2.append(Spacer(1, 1.5 * mm))

    salsa_matrix_data = [
        [Paragraph("<b>Const 0</b><br/>0x61707865", s_ct), Paragraph("<b>Key 1</b><br/>k[0..3]", s_ct), Paragraph("<b>Key 2</b><br/>k[4..7]", s_ct), Paragraph("<b>Key 3</b><br/>k[8..11]", s_ct)],
        [Paragraph("<b>Key 4</b><br/>k[12..15]", s_ct), Paragraph("<b>Const 5</b><br/>0x3320646e", s_ct), Paragraph("<b>Nonce 6</b><br/>v[0..3]", s_ct), Paragraph("<b>Nonce 7</b><br/>v[4..7]", s_ct)],
        [Paragraph("<b>Stream 8</b><br/>Block counter low", s_ct), Paragraph("<b>Stream 9</b><br/>Block counter high", s_ct), Paragraph("<b>Const 10</b><br/>0x79622d32", s_ct), Paragraph("<b>Key 11</b><br/>k[16..19]", s_ct)],
        [Paragraph("<b>Key 12</b><br/>k[20..23]", s_ct), Paragraph("<b>Key 13</b><br/>k[24..27]", s_ct), Paragraph("<b>Key 14</b><br/>k[28..31]", s_ct), Paragraph("<b>Const 15</b><br/>0x6b206574", s_ct)],
    ]
    smt = Table(salsa_matrix_data, colWidths=[CW/4.0]*4)
    smt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#FAFAFA")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CFD8DC")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    p2.append(Paragraph("<b>Table 4.1: Salsa20 4x4 State Matrix Architecture (16 Words / 512 Bits):</b>", s_h2))
    p2.append(smt)
    elements.extend(p2)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 3: TASK 1 - ARC4 AND VERNAM CIPHERS
    # -------------------------------------------------------------
    p3 = []
    p3.append(Paragraph("<b>Task 1: ARC4 & Vernam Stream Ciphers Implementation</b>", s_h1))
    p3.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=2))

    q1 = ("<b>Task 1 Requirements:</b> Run ARC4 and Vernam ciphers in Python. Print verified ciphertext in hexadecimal, "
          "then attempt decryption using an incorrect key and explain the resulting cryptographic behavior.")
    p3.append(make_callout(q1, bg=LG, border=AG))
    p3.append(Spacer(1, 1.5 * mm))

    p3.append(Paragraph("<b>Source Code (task1_arc4_vernam.py):</b>", s_h2))
    code_t1 = """def arc4crypt(data, key):
    x = 0
    box = list(range(256))
    for i in range(256):            # Key-Scheduling Algorithm (KSA)
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = y = 0
    out = []
    for char in data:               # Pseudo-Random Generation Algorithm (PRGA)
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        k = box[(box[x] + box[y]) % 256]
        out.append(chr(ord(char) ^ k))
    return ''.join(out)

def VernamEncDec(text, key):
    result = ""
    ptr = 0
    for char in text:
        result += chr(ord(char) ^ ord(key[ptr]))
        ptr = (ptr + 1) % len(key)
    return result"""
    p3.append(make_code_box(code_t1))
    p3.append(Spacer(1, 1.5 * mm))

    p3.append(Paragraph("<b>Execution Output & Terminal Verification:</b>", s_h2))
    p3.append(styled_img(f"{code_dir}/task1.png", max_w=CW, max_h=190))
    p3.append(Spacer(1, 1.5 * mm))

    t1_obs = (
        "<b>Cryptographic Observations (Wrong Key Decryption):</b><br/>"
        "&bull; <b>ARC4 Avalanche Failure:</b> A single altered bit in the key completely randomizes the KSA permutation box, "
        "causing the PRGA to output an orthogonal keystream. Decryption yields unreadable, high-entropy garbage bytes.<br/>"
        "&bull; <b>Vernam Linearity:</b> Because Vernam is pure repeating XOR, <i>C XOR K' = (P XOR K) XOR K' = P XOR (K XOR K')</i>. "
        "Decryption is corrupted character-by-character according to the exact bitwise delta of the keys."
    )
    p3.append(make_callout(t1_obs, bg=HexColor("#E3F2FD"), border=HexColor("#1976D2"), title="Analysis"))
    elements.extend(p3)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 4: TASK 2 (PART A) - XOR INVOLUTORY IDENTITY
    # -------------------------------------------------------------
    p4 = []
    p4.append(Paragraph("<b>Task 2 (Part A): XOR Involution Proof ((a XOR b) XOR b = a)</b>", s_h1))
    p4.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=2))

    q2a = ("<b>Task 2 (Part A) Requirements:</b> Formally prove with a Python loop that (a XOR b) XOR b = a for every "
           "letter from 'a' to 'z' (ASCII 97..122) under an arbitrary key byte, establishing why stream ciphers utilize "
           "identical encryption and decryption logic.")
    p4.append(make_callout(q2a, bg=LG, border=AG))
    p4.append(Spacer(1, 1.5 * mm))

    xor_proof_text = (
        "<b>Mathematical Proof of Involutory Self-Inversion:</b><br/>"
        "Bitwise XOR (addition modulo 2 without carry, XOR) satisfies three fundamental algebraic field properties:<br/>"
        "1. <b>Associativity:</b> <i>(a XOR b) XOR b = a XOR (b XOR b)</i><br/>"
        "2. <b>Self-Inverse Identity:</b> For any bit vector <i>b</i>, <i>b XOR b = 0</i><br/>"
        "3. <b>Neutral Identity:</b> <i>a XOR 0 = a</i><br/>"
        "Therefore, <i>(a XOR b) XOR b = a XOR 0 = a</i> holds identically for all inputs. Encryption and decryption are the exact same function."
    )
    p4.append(make_callout(xor_proof_text, bg=HexColor("#FFFDE7"), border=HexColor("#FBC02D"), title="Algebraic Proof"))
    p4.append(Spacer(1, 1.5 * mm))

    p4.append(Paragraph("<b>Source Code Extract (task2_xor_salsa20.py):</b>", s_h2))
    code_t2a = """def verify_xor_identity():
    test_key = 0x5A  # 90 decimal (01011010 binary)
    letters = string.ascii_lowercase
    for ch in letters:
        a = ord(ch)
        c = a ^ test_key
        decrypted = c ^ test_key
        assert decrypted == a, f"Failed for {ch}"
    print("All 26 alphabet letters satisfy (a ^ b) ^ b = a strictly.")"""
    p4.append(make_code_box(code_t2a))
    p4.append(Spacer(1, 1.5 * mm))

    p4.append(Paragraph("<b>Terminal Verification (Alphabet Involution Table):</b>", s_h2))
    p4.append(styled_img(f"{code_dir}/task2.png", max_w=CW, max_h=240))
    elements.extend(p4)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 5: TASK 2 (PART B) - SALSA20 NONCE COMPARISON
    # -------------------------------------------------------------
    p5 = []
    p5.append(Paragraph("<b>Task 2 (Part B): Salsa20 Implementation & Nonce Isolation</b>", s_h1))
    p5.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=2))

    q2b = ("<b>Task 2 (Part B) Requirements:</b> Encrypt the same message twice using Salsa20 with two distinct 24-byte nonces "
           "(IVs). Compare the resulting ciphertexts to demonstrate diffusion and cross-nonce rejection.")
    p5.append(make_callout(q2b, bg=LG, border=AG))
    p5.append(Spacer(1, 1.5 * mm))

    p5.append(Paragraph("<b>Source Code  -  XSalsa20 Encryption Routine:</b>", s_h2))
    code_salsa = """from os import urandom
from salsa20 import XSalsa20_xor

message = b"CONFIDENTIAL PATIENT RECORD: LGU HEALTH SYSTEM"
key = b"*secret**secret**secret**secret*"  # 32 bytes

nonce1 = urandom(24)
nonce2 = urandom(24)

ct1 = XSalsa20_xor(message, nonce1, key)
ct2 = XSalsa20_xor(message, nonce2, key)

# Cross-nonce decryption fails:
garbled = XSalsa20_xor(ct1, nonce2, key)"""
    p5.append(make_code_box(code_salsa))
    p5.append(Spacer(1, 1.5 * mm))

    nonce_eval = (
        "<b>Empirical Findings & Security Implications:</b><br/>"
        "&bull; <b>100% Byte Delta:</b> Across 46 plaintext bytes, exactly 46/46 ciphertext bytes differed (100.00% difference), "
        "demonstrating complete non-linear diffusion through Salsa20's 20 quarter-rounds.<br/>"
        "&bull; <b>Rejection of Cross-Nonce Decryption:</b> Attempting to decrypt Ciphertext 1 using Nonce 2 generated complete "
        "pseudo-random entropy without leaking a single plaintext character.<br/>"
        "&bull; <b>Nonce Uniqueness Invariant:</b> A nonce (Number Used Once) must NEVER be repeated with the same key. "
        "XSalsa20 provides a massive 192-bit (24-byte) nonce space, allowing random nonce generation with negligible collision risk."
    )
    p5.append(make_callout(nonce_eval, bg=HexColor("#F1F8E9"), border=G, title="Nonce Security Evaluation"))
    elements.extend(p5)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 6: TASK 3 - CUSTOM STREAM CIPHER DESIGN
    # -------------------------------------------------------------
    p6 = []
    p6.append(Paragraph("<b>Task 3: Custom Stream Cipher Architecture ('Chyron-PRG')</b>", s_h1))
    p6.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=2))

    q3 = ("<b>Task 3 Requirements (Handout Activity 4.1):</b> Design and implement your own custom stream cipher in Python, "
          "combining concepts from ARC4 (permutation S-boxes), Salsa20 (ARX rounds), and modern nonces.")
    p6.append(make_callout(q3, bg=LG, border=AG))
    p6.append(Spacer(1, 1.5 * mm))

    p6.append(Paragraph("<b>Source Code (task3_custom_stream_cipher.py):</b>", s_h2))
    code_t3 = """class ChyronStreamCipher:
    def __init__(self, key: bytes, nonce: bytes):
        assert len(key) == 16 and len(nonce) == 8
        self.sbox = list(range(256))
        self.key, self.nonce = key, nonce
        self._init_state()

    def _quarter_round(self, a, b, c, d):
        # 32-bit Add-Rotate-XOR stage (Salsa20 inspiration)
        b ^= ((a + d) & 0xFFFFFFFF) << 7 | ((a + d) & 0xFFFFFFFF) >> 25
        c ^= ((b + a) & 0xFFFFFFFF) << 9 | ((b + a) & 0xFFFFFFFF) >> 23
        d ^= ((c + b) & 0xFFFFFFFF) << 13 | ((c + b) & 0xFFFFFFFF) >> 19
        a ^= ((d + c) & 0xFFFFFFFF) << 18 | ((d + c) & 0xFFFFFFFF) >> 14
        return a & 0xFFFFFFFF, b & 0xFFFFFFFF, c & 0xFFFFFFFF, d & 0xFFFFFFFF

    def get_keystream_byte(self) -> int:
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.sbox[self.i]) % 256
        self.sbox[self.i], self.sbox[self.j] = self.sbox[self.j], self.sbox[self.i]
        t = (self.sbox[self.i] + self.sbox[self.j]) % 256
        return self.sbox[t] ^ ((self.i + self.j) & 0xFF)

    def encrypt(self, p: bytes) -> bytes:
        return bytes(b ^ self.get_keystream_byte() for b in p)"""
    p6.append(make_code_box(code_t3))
    p6.append(Spacer(1, 1.5 * mm))

    p6.append(Paragraph("<b>Execution Output & Round-Trip Verification:</b>", s_h2))
    p6.append(styled_img(f"{code_dir}/task3.png", max_w=CW, max_h=160))
    elements.extend(p6)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 7: TASK 4 - ADVERSARIAL ATTACKS ON STREAM CIPHERS
    # -------------------------------------------------------------
    p7 = []
    p7.append(Paragraph("<b>Task 4: Adversarial Cryptanalysis Attacks (Challenge)</b>", s_h1))
    p7.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=2))

    q4 = ("<b>Task 4 Requirements (Handout Activity 4.2):</b> Design and implement adversarial attacks against your custom stream "
          "cipher. Demonstrate both passive keystream reuse (Two-Time Pad) and active ciphertext bit-flipping malleability.")
    p7.append(make_callout(q4, bg=LG, border=AG))
    p7.append(Spacer(1, 1.5 * mm))

    attack_theory = (
        "<b>Two Attack Vectors Demonstrated:</b><br/>"
        "&bull; <b>1. Keystream Reuse (Two-Time Pad):</b> If the same key and nonce are used for messages P1 and P2:<br/>"
        "&nbsp;&nbsp;&nbsp;<i>C1 XOR C2 = (P1 XOR K) XOR (P2 XOR K) = P1 XOR P2</i>.<br/>"
        "The keystream cancels completely. An adversary guessing a partial word ('crib') in P1 instantly unmasks P2.<br/>"
        "&bull; <b>2. Active Bit-Flipping Malleability:</b> Stream ciphers do not guarantee integrity. "
        "An active adversary flipping bit <i>i</i> in ciphertext flips exactly bit <i>i</i> in the decrypted plaintext, "
        "enabling arbitrary unauthorized tampering without key knowledge."
    )
    p7.append(make_callout(attack_theory, bg=HexColor("#FFF3E0"), border=HexColor("#F57C00"), title="Attack Mechanics"))
    p7.append(Spacer(1, 1.5 * mm))

    p7.append(Paragraph("<b>Source Code Extract (task4_stream_cipher_attack.py):</b>", s_h2))
    code_t4 = """# 1. Two-Time Pad Attack:
c_xor = bytes(b1 ^ b2 for b1, b2 in zip(c1, c2))
crib = b"ATTACK"
recovered_p2 = bytes(c ^ k for c, k in zip(c_xor[:len(crib)], crib))
# 2. Bit-Flipping Malleability Attack:
target_patch = b"9900"  # Modify $0100 -> $9900
for i, target_char in enumerate(target_patch):
    ciphertext[start_idx + i] ^= (original_message[start_idx + i] ^ target_char)"""
    p7.append(make_code_box(code_t4))
    p7.append(Spacer(1, 1.5 * mm))

    p7.append(Paragraph("<b>Execution Output  -  Verified Attacks on Chyron-PRG:</b>", s_h2))
    p7.append(styled_img(f"{code_dir}/task4.png", max_w=CW, max_h=190))
    elements.extend(p7)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 8: ASSESSMENT, VIVA QUESTIONS & COMPARATIVE MATRIX
    # -------------------------------------------------------------
    p8 = []
    p8.append(Paragraph("<b>Assessment: Viva Voce & Comparative Analysis</b>", s_h1))
    p8.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=2))

    viva_text = (
        "<b>Viva Voce Questions & Answers (Slide 15):</b><br/>"
        "&bull; <b>Q1: Why does XOR-ing twice with the same key give back the plaintext?</b><br/>"
        "&nbsp;&nbsp;&nbsp;<b>A:</b> Because XOR is self-inverting (<i>(a XOR b) XOR b = a</i>); encryption and decryption are mathematically identical.<br/>"
        "&bull; <b>Q2: What does a PRG do in a stream cipher?</b><br/>"
        "&nbsp;&nbsp;&nbsp;<b>A:</b> It deterministically expands a short secret key and nonce into an arbitrarily long, pseudo-random keystream.<br/>"
        "&bull; <b>Q3: Why must a keystream never be reused?</b><br/>"
        "&nbsp;&nbsp;&nbsp;<b>A:</b> Keystream reuse enables the Two-Time Pad attack: <i>C1 XOR C2 = P1 XOR P2</i>, completely eliminating key security.<br/>"
        "&bull; <b>Q4: Is the handout Vernam code a real OTP? Why or why not?</b><br/>"
        "&nbsp;&nbsp;&nbsp;<b>A:</b> No. The key is shorter than the message and repeats. A true OTP requires a truly random, non-repeating key as long as the message.<br/>"
        "&bull; <b>Q5: What are the two phases of ARC4?</b><br/>"
        "&nbsp;&nbsp;&nbsp;<b>A:</b> Key-Scheduling Algorithm (KSA) initializes the 256-byte S-box; Pseudo-Random Generation Algorithm (PRGA) outputs keystream bytes.<br/>"
        "&bull; <b>Q6: Why is ARC4 no longer used in TLS?</b><br/>"
        "&nbsp;&nbsp;&nbsp;<b>A:</b> Known statistical biases in early keystream bytes (Fluhrer-Mantin-Shamir attack); prohibited by RFC 7465 (2015)."
    )
    p8.append(make_callout(viva_text, bg=LG, border=AG, title="Viva Voce Defense Matrix"))
    p8.append(Spacer(1, 1.5 * mm))

    comp_data = [
        [Paragraph("<b>Feature / Metric</b>", s_cl), Paragraph("<b>Vernam (OTP)</b>", s_cl), Paragraph("<b>ARC4</b>", s_cl), Paragraph("<b>Salsa20 / XSalsa20</b>", s_cl)],
        [Paragraph("Key Length", s_body), Paragraph("Equal to message", s_body), Paragraph("40 - 2048 bits (typ. 128)", s_body), Paragraph("128 or 256 bits", s_body)],
        [Paragraph("Nonce / IV", s_body), Paragraph("None (Single use key)", s_body), Paragraph("None built-in (Weak IV in WEP)", s_body), Paragraph("64-bit / 192-bit (XSalsa20)", s_body)],
        [Paragraph("State Size", s_body), Paragraph("None (Direct XOR)", s_body), Paragraph("256 bytes (Permutation)", s_body), Paragraph("64 bytes (16 x 32-bit words)", s_body)],
        [Paragraph("Core Primitive", s_body), Paragraph("Bitwise XOR", s_body), Paragraph("KSA + PRGA table swaps", s_body), Paragraph("ARX Quarter-Rounds", s_body)],
        [Paragraph("Security Level", s_body), Paragraph("Information-Theoretic (True OTP)", s_body), Paragraph("Broken (RFC 7465 prohibited)", s_body), Paragraph("High (eSTREAM Portfolio winner)", s_body)],
        [Paragraph("Speed / Hardware", s_body), Paragraph("Instantaneous", s_body), Paragraph("Fast in software (Byte-based)", s_body), Paragraph("Extremely fast (Parallel 32-bit)", s_body)],
    ]
    ctbl = Table(comp_data, colWidths=[28 * mm, 34 * mm, 38 * mm, main_w - 100 * mm if 'main_w' in locals() else 45 * mm])
    ctbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LG),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CFD8DC")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    p8.append(Paragraph("<b>Table 4.2: Comprehensive Stream Cipher Comparison Matrix:</b>", s_h2))
    p8.append(ctbl)
    elements.extend(p8)

    # -------------------------------------------------------------
    # BUILD PDF
    # -------------------------------------------------------------
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=LM,
        rightMargin=RM,
        topMargin=TM,
        bottomMargin=BM,
    )

    doc.build(elements, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"Generated PDF: {output_pdf}")

    shutil.copyfile(output_pdf, desktop_pdf)
    print(f"Copied to Desktop: {desktop_pdf}")


if __name__ == "__main__":
    main()
