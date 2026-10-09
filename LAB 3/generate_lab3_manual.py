#!/usr/bin/env python3
"""
Information Security Lab - Lab Manual 03 Generator
Author: Muhammad Fezan (Fall-23-BSCS-466)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Course: Information Security Lab (7th Semester - Fall 2026)
Institution: Lahore Garrison University - Department of Computer Science
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

# === COLORS ===
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
CW = PAGE_W - LM - RM   # Content width: 451.27 pt
SB_W = 12 * mm           # Sidebar width on cover

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
    fontSize=7.5,
    leading=9.5,
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
    canvas.drawString(LM, PAGE_H - 0.6 * inch, "Information Security Lab  |  Lab Manual 03  -  Classical Cryptography & Cryptanalysis")
    canvas.setStrokeColor(HexColor("#E0E0E0"))
    canvas.setLineWidth(0.5)
    canvas.line(LM, PAGE_H - 0.65 * inch, PAGE_W - RM, PAGE_H - 0.65 * inch)
    canvas.drawCentredString(PAGE_W / 2, 0.5 * inch, f"Page {canvas.getPageNumber()}  |  M.Fezan  |  Fall-23-BSCS-466")
    canvas.restoreState()

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
    main_items.append(Paragraph("LAB MANUAL # 3", s_ctt))
    main_items.append(Paragraph("Classical Ciphers & Cryptanalysis (Affine, Multiplicative, CrypTool 2 & Transposition)", s_cs))
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
        [Paragraph("<b>CONTEXT:</b>", s_cl), Paragraph("Lab Manual # 3 - Graded Practical Tasks & Cryptanalysis", s_cv)],
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

# === HELPER: IMAGE RESIZER ===
def styled_img(path, max_w, max_h):
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

def main():
    code_dir = "/home/honeypot/Univeristy_Data/IS(L)/LAB 3/Code"
    output_pdf = "/home/honeypot/Univeristy_Data/IS(L)/LAB 3/Information_Security_Lab_Manual_03.pdf"
    desktop_pdf = "/home/honeypot/Desktop/Information_Security_Lab_Manual_03.pdf"

    elements = build_cover()

    # -------------------------------------------------------------
    # PAGE 2: TASK 1 - AFFINE CIPHER CHALLENGE
    # -------------------------------------------------------------
    t1_items = []
    t1_items.append(Paragraph("<b>Task 1: Affine Cipher Challenge</b>", s_h1))
    t1_items.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=2))
    
    q1 = ("<b>Question #1:</b> Implement the Affine cipher: multiply by key A, add key B, mod the symbol-set "
          "size to encrypt; reverse with the modular inverse of A to decrypt. Ensure key A is coprime to 26 "
          "(gcd(a, 26) = 1) and preserve all non-alphabetic casing and symbols. Include code and verified output.<br/>"
          "<b>Mathematical Formulation:</b> <i>C = (a * P + b) mod 26</i> &nbsp;|&nbsp; <i>P = a<sup>-1</sup> * (C - b) mod 26</i>. "
          "For keys <i>a = 5, b = 8</i>: <i>gcd(5, 26) = 1</i>, yielding modular inverse <i>a<sup>-1</sup> = 21</i> since <i>(5 * 21) == 1 (mod 26)</i>.")
    t1_items.append(make_callout(q1, bg=LG, border=AG))
    t1_items.append(Spacer(1, 1.5 * mm))

    t1_items.append(Paragraph("<b>Source Code (task1_affine_cipher.py):</b>", s_h2))
    t1_code = """import math
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
M = 26

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt_affine(plaintext, a, b):
    if math.gcd(a, M) != 1:
        raise ValueError(f"Key 'a' ({a}) must be coprime to {M}.")
    ciphertext = []
    for char in plaintext:
        if char.isalpha():
            is_upper = char.isupper()
            x = ALPHABET.index(char.lower())
            cipher_char = ALPHABET[(a * x + b) % M]
            ciphertext.append(cipher_char.upper() if is_upper else cipher_char)
        else:
            ciphertext.append(char)
    return ''.join(ciphertext)

def decrypt_affine(ciphertext, a, b):
    a_inv = mod_inverse(a, M)
    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            is_upper = char.isupper()
            y = ALPHABET.index(char.lower())
            plain_char = ALPHABET[(a_inv * (y - b)) % M]
            plaintext.append(plain_char.upper() if is_upper else plain_char)
        else:
            plaintext.append(char)
    return ''.join(plaintext)"""
    t1_items.append(make_code_box(t1_code))
    t1_items.append(Spacer(1, 1.5 * mm))

    t1_items.append(Paragraph("<b>Execution Output (Terminal Verification):</b>", s_h2))
    t1_items.append(styled_img(f"{code_dir}/task1.png", max_w=CW, max_h=180))
    elements.extend(t1_items)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 3: TASK 2 (PART 1) - MULTIPLICATIVE CIPHER IMPLEMENTATION
    # -------------------------------------------------------------
    t2_p1_items = []
    t2_p1_items.append(Paragraph("<b>Task 2: Multiplicative Cipher & Cryptanalysis</b>", s_h1))
    t2_p1_items.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=3))

    q2 = ("<b>Question #2:</b> Implement (letter x key) mod 26 with key = 7, then explain and demonstrate "
          "how the cipher can be broken using brute force and statistical frequency cryptanalysis.")
    t2_p1_items.append(make_callout(q2, bg=LG, border=AG))
    t2_p1_items.append(Spacer(1, 2 * mm))

    m2_desc = (
        "<b>Cipher Mechanics & Parameters:</b><br/>"
        "&bull; <b>Encryption Formula:</b> <i>C = (P * key) mod 26</i> &nbsp;|&nbsp; Key <i>k = 7</i>.<br/>"
        "&bull; <b>Decryption Formula:</b> <i>P = (C * key<sup>-1</sup>) mod 26</i> &nbsp;|&nbsp; Inverse <i>k<sup>-1</sup> = 15</i> (since 7 * 15 = 105 == 1 mod 26).<br/>"
        "&bull; <b>Vulnerability Overview:</b> Only 12 coprime integers exist in modulo 26, creating an extremely trivial key space."
    )
    t2_p1_items.append(make_callout(m2_desc, bg=HexColor("#F1F8E9"), border=G))
    t2_p1_items.append(Spacer(1, 2 * mm))

    t2_p1_items.append(Paragraph("<b>Source Code  -  Cipher Implementation:</b>", s_h2))
    t2_code_core = """import math
from collections import Counter

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
M = 26
VALID_KEYS = [k for k in range(1, M) if math.gcd(k, M) == 1]  # 12 Coprime Keys

def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt_multiplicative(plaintext, key=7):
    ciphertext = []
    for char in plaintext:
        if char.isalpha():
            is_upper = char.isupper()
            cipher_idx = (ALPHABET.index(char.lower()) * key) % M
            c = ALPHABET[cipher_idx]
            ciphertext.append(c.upper() if is_upper else c)
        else:
            ciphertext.append(char)
    return ''.join(ciphertext)

def decrypt_multiplicative(ciphertext, key=7):
    key_inv = mod_inverse(key, M)
    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            is_upper = char.isupper()
            plain_idx = (ALPHABET.index(char.lower()) * key_inv) % M
            p = ALPHABET[plain_idx]
            plaintext.append(p.upper() if is_upper else p)
        else:
            plaintext.append(char)
    return ''.join(plaintext)"""
    t2_p1_items.append(make_code_box(t2_code_core))
    t2_p1_items.append(Spacer(1, 2 * mm))

    t2_p1_items.append(Paragraph("<b>Execution Output  -  Part 1: Encryption & Decryption:</b>", s_h2))
    t2_p1_items.append(styled_img(f"{code_dir}/task2_part1.png", max_w=CW, max_h=165))
    elements.extend(t2_p1_items)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 4: TASK 2 (PART 2) - CRYPTANALYSIS DEMONSTRATION
    # -------------------------------------------------------------
    t2_p2_items = []
    t2_p2_items.append(Paragraph("<b>Task 2: Cryptanalysis Attacks (Hacking the Multiplicative Cipher)</b>", s_h1))
    t2_p2_items.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=3))

    h_desc = (
        "<b>Two Attack Methodologies Demonstrated:</b><br/>"
        "1. <b>Exhaustive Brute-Force Search:</b> Because <i>gcd(k, 26) = 1</i>, only 12 valid keys exist: "
        "<i>[1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]</i>. An attacker computes all 12 plaintexts in microseconds.<br/>"
        "2. <b>Statistical Frequency Cryptanalysis:</b> The most frequent ciphertext letter is assumed to be 'E' (index 4). "
        "Solving the linear congruence <i>(4 * k) == C<sub>max</sub> (mod 26)</i> immediately exposes the secret key."
    )
    t2_p2_items.append(make_callout(h_desc, bg=HexColor("#FFFDE7"), border=HexColor("#FBC02D"), title="Vulnerability Analysis"))
    t2_p2_items.append(Spacer(1, 2 * mm))

    t2_p2_items.append(Paragraph("<b>Source Code  -  Cryptanalysis Attack Routines:</b>", s_h2))
    t2_code_hack = """def attack_brute_force(ciphertext):
    print("--- Exhaustive Brute-Force Attack (12 Coprime Keys) ---")
    results = []
    for candidate_key in VALID_KEYS:
        candidate_inv = mod_inverse(candidate_key, M)
        decrypted = decrypt_multiplicative(ciphertext, candidate_key)
        results.append((candidate_key, candidate_inv, decrypted))
    return results

def attack_frequency_analysis(ciphertext):
    print("--- Frequency Analysis Attack (Mapping C_max -> 'E') ---")
    letters = [c.lower() for c in ciphertext if c.isalpha()]
    most_common_char, freq = Counter(letters).most_common(1)[0]
    c_idx = ALPHABET.index(most_common_char)
    # Solve linear congruence: (4 * key) % 26 == c_idx
    candidate_keys = [k for k in VALID_KEYS if (4 * k) % M == c_idx]
    for k in candidate_keys:
        print(f"Candidate Key: {k} -> Decryption: {decrypt_multiplicative(ciphertext, k)[:45]}...")"""
    t2_p2_items.append(make_code_box(t2_code_hack))
    t2_p2_items.append(Spacer(1, 2 * mm))

    t2_p2_items.append(Paragraph("<b>Execution Output  -  Part 2: Brute-Force & Frequency Analysis Attack Output:</b>", s_h2))
    t2_p2_items.append(styled_img(f"{code_dir}/task2_part2.png", max_w=CW, max_h=215))
    elements.extend(t2_p2_items)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 5: TASK 3 (PART 1) - CRYPTOOL 2 VIGENERE & ANALYZER
    # -------------------------------------------------------------
    t3_p1_items = []
    t3_p1_items.append(Paragraph("<b>Task 3: CrypTool 2 Exploration & Cryptanalysis (Part 1)</b>", s_h1))
    t3_p1_items.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=3))

    q3 = ("<b>Question #3:</b> Use the CrypTool app to encrypt/decrypt with Vigenere, then practice "
          "frequency analysis and known-plaintext cryptanalysis on this lab's ciphers.")
    t3_p1_items.append(make_callout(q3, bg=LG, border=AG))
    t3_p1_items.append(Spacer(1, 2 * mm))

    t3_obs1 = (
        "<b>CrypTool 2 Workflow & Observations:</b><br/>"
        "&bull; <b>Workspace 1 (Vigenere Encryption/Decryption):</b> Configured visual pipeline with Plaintext Input, "
        "Key (<i>SECRETKEY</i>), Vigenere Encryption component, and Decryption round-trip verifying exact recovery.<br/>"
        "&bull; <b>Workspace 2 (Vigenere Analyzer):</b> Executed automated statistical cryptanalysis using hill-climbing optimization. "
        "CrypTool successfully computed Chi-Square (Chi^2) scores, detected key length, and recovered key <b>SECRETKEYS</b> in 0.05 min."
    )
    t3_p1_items.append(make_callout(t3_obs1, bg=HexColor("#E3F2FD"), border=HexColor("#1976D2"), title="Methodology & Tooling"))
    t3_p1_items.append(Spacer(1, 2 * mm))

    t3_p1_items.append(Paragraph("<b>Figure 3.1: CrypTool 2  -  Vigenere Cipher Encryption & Round-Trip Decryption:</b>", s_h2))
    t3_p1_items.append(styled_img(f"{code_dir}/task3_part1.png", max_w=CW, max_h=170))
    t3_p1_items.append(Spacer(1, 2 * mm))

    t3_p1_items.append(Paragraph("<b>Figure 3.2: CrypTool 2  -  Automated Cryptanalysis & Key Recovery (Vigenere Analyzer):</b>", s_h2))
    t3_p1_items.append(styled_img(f"{code_dir}/task3_part2.png", max_w=CW, max_h=170))
    elements.extend(t3_p1_items)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 6: TASK 3 (PART 2) - STATISTICAL FREQUENCY ANALYSIS
    # -------------------------------------------------------------
    t3_p2_items = []
    t3_p2_items.append(Paragraph("<b>Task 3: CrypTool 2 Exploration  -  Frequency Analysis (Part 2)</b>", s_h1))
    t3_p2_items.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=3))

    freq_exp = (
        "<b>Statistical Frequency Analysis Theory & Findings:</b><br/>"
        "&bull; <b>Unigram Distribution (Single Letters):</b> In natural English, letters exhibit highly non-uniform frequencies: "
        "<b>E</b> dominates at ~13.17%, followed by <b>T</b> (~9.82%), <b>A</b> (~8.1%), and <b>O</b> (~7.5%). Monoalphabetic substitution "
        "preserves this distribution shape completely, enabling instant key extraction.<br/>"
        "&bull; <b>Bigram Distribution (Digraph Pairs):</b> Common two-letter pairings like <b>TH</b> (2.96%), <b>HE</b> (2.71%), and <b>IN</b> "
        "provide secondary confirmation for cryptanalysts when attacking polyalphabetic or transposed ciphers.<br/>"
        "&bull; <b>Vigenere Flattening Effect:</b> Unlike monoalphabetic ciphers, Vigenere uses multiple Caesar shifts across characters, "
        "flattening the frequency distribution and requiring key-length determination (Kasiski/Friedman tests) prior to frequency extraction."
    )
    t3_p2_items.append(make_callout(freq_exp, bg=HexColor("#F3E5F5"), border=HexColor("#7B1FA2"), title="Cryptanalytic Frequency Profile"))
    t3_p2_items.append(Spacer(1, 2 * mm))

    t3_p2_items.append(Paragraph("<b>Figure 3.3: CrypTool 2  -  Unigram & Bigram Frequency Analysis Histograms:</b>", s_h2))
    t3_p2_items.append(styled_img(f"{code_dir}/task3_part3.png", max_w=CW, max_h=230))
    t3_p2_items.append(Spacer(1, 2 * mm))

    comp_table_data = [
        [Paragraph("<b>Cipher Scheme</b>", s_cl), Paragraph("<b>Type</b>", s_cl), Paragraph("<b>Key Space</b>", s_cl), Paragraph("<b>Frequency Resistance</b>", s_cl)],
        [Paragraph("Caesar Cipher", s_body), Paragraph("Monoalphabetic", s_body), Paragraph("25 keys", s_body), Paragraph("Zero (Exact shift preserved)", s_body)],
        [Paragraph("Multiplicative", s_body), Paragraph("Monoalphabetic", s_body), Paragraph("12 coprime keys", s_body), Paragraph("Zero (Single peak mapping)", s_body)],
        [Paragraph("Affine Cipher", s_body), Paragraph("Monoalphabetic", s_body), Paragraph("312 keys (12 x 26)", s_body), Paragraph("Low (Two frequency points break key)", s_body)],
        [Paragraph("Vigenere Cipher", s_body), Paragraph("Polyalphabetic", s_body), Paragraph("26<sup>L</sup> (L = key length)", s_body), Paragraph("Moderate (Flattened; broken via Kasiski)", s_body)],
        [Paragraph("Transposition", s_body), Paragraph("Permutation", s_body), Paragraph("K! column permutations", s_body), Paragraph("High (Unigrams preserved, bigrams broken)", s_body)],
    ]
    ctbl = Table(comp_table_data, colWidths=[30 * mm, 32 * mm, 42 * mm, main_w - 104 * mm if 'main_w' in locals() else 55 * mm])
    ctbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LG),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CFD8DC")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    t3_p2_items.append(Paragraph("<b>Comparative Analysis of Classical Ciphers:</b>", s_h2))
    t3_p2_items.append(ctbl)
    elements.extend(t3_p2_items)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 7: TASK 4 (PART 1) - EXTENDED TRANSPOSITION CIPHER
    # -------------------------------------------------------------
    t4_p1_items = []
    t4_p1_items.append(Paragraph("<b>Task 4: Extended Transposition Cipher Challenge (Implementation)</b>", s_h1))
    t4_p1_items.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=3))

    q4 = ("<b>Question #4:</b> Extend the Columnar Transposition Cipher with 6 challenge enhancements:<br/>"
          "1. Handle key / plaintext length mismatch gracefully.<br/>"
          "2. Implement an inverse <i>decode()</i> / decrypt routine.<br/>"
          "3. Preserve original letter casing throughout encryption.<br/>"
          "4. Retain spaces, numbers, and punctuation marks without loss.<br/>"
          "5. Generate a cryptographically randomized column key.<br/>"
          "6. Provide an interactive Command Line Interface (CLI) menu system.")
    t4_p1_items.append(make_callout(q4, bg=LG, border=AG))
    t4_p1_items.append(Spacer(1, 2 * mm))

    t4_desc = (
        "<b>Transposition Algorithm Architecture:</b><br/>"
        "&bull; <b>Geometry:</b> Grid dimensions are <i>num_cols = key</i> and <i>num_rows = ceil(len(text) / key)</i>.<br/>"
        "&bull; <b>Length Mismatch & Shaded Cells:</b> When <i>len(text) % key != 0</i>, the last row has empty 'shaded' cells "
        "equal to <i>(num_rows * num_cols) - len(text)</i>. The decoding algorithm tracks shaded cells to reconstruct exact column boundaries."
    )
    t4_p1_items.append(make_callout(t4_desc, bg=HexColor("#F1F8E9"), border=G, title="Grid Geometry & Inversion Logic"))
    t4_p1_items.append(Spacer(1, 2 * mm))

    t4_p1_items.append(Paragraph("<b>Source Code  -  Transposition Core (Sub-tasks 1, 2, 3, 4, 5):</b>", s_h2))
    t4_code_core = """import math, random

def generate_random_key(min_key=3, max_key=8):
    return random.randint(min_key, max_key)  # Sub-task 5

def encode_transposition(plaintext, key, pad_char=''):
    # Sub-tasks 1, 3, 4: Preserves spaces/casing, handles length mismatch
    text = plaintext
    if pad_char and len(text) % key != 0:
        text += pad_char * (key - (len(text) % key))
    ciphertext = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(text):
            ciphertext[col] += text[pointer]
            pointer += key
    return ''.join(ciphertext)

def decode_transposition(ciphertext, key):
    # Sub-task 2: Inverse decode() handling irregular column boundaries
    total_len = len(ciphertext)
    num_rows = math.ceil(total_len / key)
    num_cols = key
    num_shaded_boxes = (num_rows * num_cols) - total_len
    plaintext = [''] * num_rows
    col = row = 0
    for symbol in ciphertext:
        plaintext[row] += symbol
        col += 1
        if (col == num_cols) or (col == num_cols - 1 and row >= num_rows - num_shaded_boxes):
            col = 0
            row += 1
    return ''.join(plaintext)"""
    t4_p1_items.append(make_code_box(t4_code_core))
    elements.extend(t4_p1_items)
    elements.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 8: TASK 4 (PART 2) - VERIFICATION & CLI MENU
    # -------------------------------------------------------------
    t4_p2_items = []
    t4_p2_items.append(Paragraph("<b>Task 4: Transposition Cipher  -  Verification & CLI Interface</b>", s_h1))
    t4_p2_items.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=3))

    t4_p2_items.append(Paragraph("<b>Source Code  -  Interactive Menu & Self-Test (Sub-task 6):</b>", s_h2))
    t4_code_menu = """def menu():
    while True:
        print("\\n=== INFOSEC LAB 03: TRANSPOSITION CIPHER MENU ===")
        print("  1. Encrypt Message  |  2. Decrypt Message")
        print("  3. Random Key       |  4. Full Self-Test Demo  |  5. Exit")
        choice = input("Enter choice (1-5): ").strip()
        if choice == '1':
            msg, k = input("Text: "), int(input("Key (columns): "))
            print(f"[+] Ciphertext: {encode_transposition(msg, k)}")
        elif choice == '2':
            ct, k = input("Ciphertext: "), int(input("Key: "))
            print(f"[+] Decrypted: {decode_transposition(ct, k)}")
        elif choice == '3':
            print(f"[+] Generated Random Key: {generate_random_key(3, 10)}")
        elif choice == '4':
            run_self_test()
        elif choice == '5':
            break"""
    t4_p2_items.append(make_code_box(t4_code_menu))
    t4_p2_items.append(Spacer(1, 2 * mm))

    t4_p2_items.append(Paragraph("<b>Execution Output  -  Verification of All 6 Challenge Sub-tasks:</b>", s_h2))
    t4_p2_items.append(styled_img(f"{code_dir}/task4.png", max_w=CW, max_h=235))
    t4_p2_items.append(Spacer(1, 2 * mm))

    t4_summary = (
        "<b>Verification Results:</b><br/>"
        "&bull; <b>Mismatch & Round-Trip:</b> 73-character sentence evaluated against key=6 (<i>73 mod 6 = 1</i> mismatch); "
        "decoded with <b>100% exact character reconstruction</b>.<br/>"
        "&bull; <b>Symbol Fidelity:</b> Uppercase, lowercase, commas, periods, and exclamation marks preserved intact.<br/>"
        "&bull; <b>Random Key:</b> Automated key generation dynamically created random column widths with zero cipher degradation."
    )
    t4_p2_items.append(make_callout(t4_summary, bg=LG, border=AG, title="Automated Integrity Verification"))
    elements.extend(t4_p2_items)

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
