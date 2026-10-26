#!/usr/bin/env python3
"""
Information Security Lab - Lab Manual 06 Generator
Author: Muhammad Fezan (Fall-23-BSCS-466)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Course: Information Security Lab (7th Semester - Fall 2026)
Topic: Secure Hash Functions - birthday attack, SHA-256 collision resistance,
       PBKDF2 hash stretching, salted password storage and verification.
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

LAB_DIR = "/home/honeypot/Univeristy_Data/IS(L)/LAB 6"
SOL_DIR = os.path.join(LAB_DIR, "solution")
SHOT_DIR = os.path.join(SOL_DIR, "shots")
LOGO_PATH = "/home/honeypot/.hermes/skills/lgu-assignment/assets/lgu-logo.png"
OUT_PDF = os.path.join(LAB_DIR, "Information_Security_Lab_Manual_06.pdf")

RUNNING_HEAD = ("Information Security Lab  |  Lab Manual 06  -  Secure Hash "
                "Functions, Birthday Attacks & Password Hashing")


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
s_h1.keepWithNext = 1
s_h2 = S("h2", size=9.8, color=AG, bold=True, sa=2, sb=5)
s_h2.keepWithNext = 1
s_body = S("body", size=9, color=TD, sa=2.5, leading=12.5, align=TA_JUSTIFY)
s_bul = S("bul", size=9, color=TD, sa=1.5, leading=12.2, li=12)
s_callout = S("callout", size=8.6, color=TD, sa=0, leading=11.6)
s_cap = S("cap", size=8, color=SG, align=TA_CENTER, italic=True, sa=6, sb=2)
s_tb = S("tb", size=8.4, color=TD, sa=0, leading=10.6)
s_th = S("th", size=8.4, color=HexColor("#FFFFFF"), align=TA_CENTER, bold=True, sa=0)

code_style = ParagraphStyle("CodeStyle", fontName="Courier", fontSize=6.3,
                            leading=7.5, textColor=NAVY)


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
    canvas.drawString(LM, PAGE_H - 0.6 * inch, RUNNING_HEAD)
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
        out.append(Spacer(1, 4))
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
    return KeepTogether([tbl])


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
    items.append(Paragraph("LAB MANUAL # 6", s_ctt))
    items.append(Paragraph("Secure Hash Functions: Birthday Attack, SHA-256 Collision "
                           "Resistance, PBKDF2 Hash Stretching &amp; Salted Password Storage", s_cs))
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
        [Paragraph("<b>CONTEXT:</b>", s_cl), Paragraph("Lab Manual # 6 - Secure Hash Functions (Week 06 task sheet)", s_cv)],
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
    e.append(Paragraph("Lab 06 - Objectives and Scope", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "A cryptographic hash function maps a message of any length to a fixed-size digest. "
        "Unlike encryption it takes no key and cannot be reversed: the only way to produce a "
        "given digest is to guess the message. That one property supports integrity checks, "
        "digital signatures, message authentication codes and password storage, and every one of "
        "those uses collapses if two different messages can be made to hash to the same value. "
        "This lab therefore attacks SHA-256 directly rather than describing it: first by "
        "truncating it until collisions become cheap, then by attempting the same attack on the "
        "full digest, and finally by applying the primitive where it matters most - storing "
        "passwords.", s_body))
    e.append(Spacer(1, 2))
    e.append(Paragraph("Learning outcomes (CLO 4 / C4):", s_h2))
    for t in [
        "State the three security properties of a hash function (preimage, second preimage, "
        "collision resistance) and the work factor each one implies for a b-bit digest.",
        "Derive the birthday bound sqrt(pi/2 * 2^b) and use it to explain why a hash gives only "
        "b/2 bits of collision security.",
        "Implement a birthday attack on a 16-bit truncated SHA-256 and measure how many messages "
        "are needed in practice.",
        "Run a collision search over one million messages on the complete 256-bit digest and "
        "interpret the result quantitatively.",
        "Apply PBKDF2-HMAC-SHA256 with different iteration counts, measure the cost, and relate "
        "it to an attacker's guessing rate.",
        "Store and verify a password with a random per-user salt, and explain why the salt "
        "defeats precomputed rainbow tables.",
    ]:
        e.append(Paragraph(f"&bull; {t}", s_bul))
    e.append(Spacer(1, 4))

    e.append(make_callout(
        "<b>Environment used for every task:</b> Python 3.11 with the standard <i>hashlib</i> "
        "module (backed by OpenSSL 3.x) inside the Hermes virtual environment at "
        "/home/honeypot/.hermes/hermes-agent/venv. No third-party cryptography package is needed: "
        "SHA-256 and PBKDF2 are both part of the standard library. All screenshots in this manual "
        "are real program output, captured from the terminal and rendered with Pillow, then "
        "embedded with ReportLab.", title="Tooling"))

    # ---------------- Theory ----------------
    e.append(Paragraph("1. Hash Functions and the Birthday Bound", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "Three properties are demanded of a cryptographic hash, and each has a different price "
        "for the attacker. The digest length is chosen by the weakest of them, because that is "
        "the one that breaks first.", s_body))
    e.append(Spacer(1, 2))

    e.append(make_table(
        ["Property", "Definition", "Attack cost, b-bit digest"],
        [
            ["Preimage resistance",
             "Given h, find any m with H(m) = h.",
             "2^b - exhaustive search over messages."],
            ["Second preimage resistance",
             "Given m1, find m2 != m1 with H(m1) = H(m2).",
             "2^b - the target digest is fixed."],
            ["Collision resistance",
             "Find any pair m1 != m2 with H(m1) = H(m2).",
             "2^(b/2) - the birthday bound."],
            ["Avalanche effect",
             "One flipped input bit changes about half of the output bits.",
             "Not an attack, but required for diffusion."],
        ],
        [105, 195, CW - 300]))
    e.append(Spacer(1, 4))

    e.append(Paragraph("1.1 Why collisions are the cheap attack", s_h2))
    e.append(Paragraph(
        "Preimage resistance costs 2^b because the attacker must land on one exact value. A "
        "collision only requires <b>any two</b> messages to land on the <b>same</b> value, and "
        "there are n(n-1)/2 pairs among n messages. Setting that equal to the size of the digest "
        "space gives n = sqrt(2 * 2^b), so the search collapses from exponential in b to "
        "exponential in b/2. The exact probability after n messages is", s_body))
    e.append(Paragraph(
        "P(collision) = 1 - exp( -n(n-1) / 2^(b+1) ),   and the median is sqrt(pi/2 * 2^b).",
        S("formula", font="Courier", size=8.6, color=NAVY, align=TA_CENTER, sa=4, sb=2)))
    e.append(Paragraph(
        "For a 16-bit tag the median is 321 messages; for SHA-256 it is 2^128, which is why a "
        "256-bit hash is described as having 128-bit collision security. Figure 1 plots the "
        "curve for b = 16 and marks the collision that Task 1 actually found.", s_body))
    e.append(Spacer(1, 2))
    for f in shot("diagram_birthday.png",
                  "Fig. 1: Collision probability against the number of hashed messages for a "
                  "16-bit tag. The measured collision (230 messages) sits on the theoretical curve.",
                  max_h=250):
        e.append(f)

    e.append(Paragraph("1.2 What SHA-256 does with the message", s_h2))
    e.append(Paragraph(
        "SHA-256 follows the Merkle-Damgard construction. The message is padded with a single 1 "
        "bit, then zeros, then its original length as a 64-bit integer, so that the total is a "
        "multiple of 512 bits. Each 512-bit block is fed into a compression function that updates "
        "eight 32-bit state words over 64 rounds of additions, rotations and bitwise choice "
        "operations; the message schedule expands the 16 input words into 64 round words. The "
        "digest is the final state, 32 bytes. Because every block is folded into the state, "
        "changing one input bit changes the entire digest, which is the avalanche property the "
        "table above lists.", s_body))
    e.append(Spacer(1, 2))
    e.append(make_callout(
        "The same chaining construction allows a <b>length-extension attack</b>: given H(m) and "
        "the length of m, an attacker can compute H(m || pad || x) without knowing m. This is why "
        "a MAC must never be built as H(key || message); HMAC wraps the key twice instead. The "
        "lab does not exploit it, but it is the reason HMAC appears in the PBKDF2 tasks.",
        bg=HexColor("#FFF8E1"), border=HexColor("#B08800"), title="Construction note"))
    e.append(PageBreak())

    # ---------------- Task 1 ----------------
    e.append(Paragraph("Task 1 - Birthday Attack on a 16-bit Truncated SHA-256", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "<b>Requirement:</b> simulate a birthday attack by truncating SHA-256 hashes to 16 bits "
        "and detecting a collision between two different messages.", s_body))
    e.append(Spacer(1, 4))
    e.append(KeepTogether([Paragraph("Execution output", s_h2)] +
                          shot("shot_task1.png",
                               "Fig. 2: Task 1 run - two different messages share the tag 0x1293 "
                               "while their full 256-bit digests differ, plus the statistics over "
                               "200 independent trials.", max_h=520)))
    e.append(Spacer(1, 4))
    e.append(Paragraph("Implementation (task1_birthday_attack.py)", s_h2))
    e.extend(make_code_blocks(read_code("task1_birthday_attack.py"), 4))
    e.append(Spacer(1, 2))
    e.append(Paragraph(
        "The program keeps a dictionary keyed by the 16-bit tag. Every new message is hashed, its "
        "first two bytes are used as the key, and a key that already exists is the collision. "
        "Messages are built from a counter plus a 48-bit random nonce, so no two messages can ever "
        "be identical and the only possible reason for a repeated tag is a genuine hash collision.",
        s_body))


    e.append(Paragraph("Result analysis", s_h2))
    e.append(Paragraph(
        "The collision appeared after 230 messages in 1.08 ms. Message A and message B differ in "
        "the counter and in the nonce, their full SHA-256 digests share no visible structure, yet "
        "both begin with the byte pair 0x1293. The program verifies all three facts explicitly: "
        "the messages differ, the truncated tags are equal, and the complete digests are not. "
        "That last line is the important one - the attack found a collision in the tag, not in "
        "SHA-256 itself.", s_body))
    e.append(Spacer(1, 2))
    e.append(make_table(
        ["Statistic", "Value"],
        [
            ["Messages hashed before the collision", "230"],
            ["Collision probability at that point", "33.09%"],
            ["Time to find it", "1.08 ms"],
            ["Full digests equal", "False - only the 16-bit prefix matches"],
            ["Mean over 200 trials", "336.2 messages (theory 320.8, +4.8%)"],
            ["Median / quartiles", "302 / 207 / 439 messages"],
            ["Minimum and maximum", "18 and 1,200 messages"],
        ],
        [150, CW - 150]))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "The measured mean agrees with sqrt(pi/2 * 2^16) = 320.8 to within five percent, which "
        "confirms that the birthday bound is a practical prediction and not a loose upper limit. "
        "The distribution is heavy-tailed: the minimum over 200 trials was 18 messages and the "
        "maximum 1,200, a spread of almost two orders of magnitude, so a single run says very "
        "little and only the mean over many runs can be compared with theory.", s_body))
    e.append(Spacer(1, 4))
    e.append(make_callout(
        "A 16-bit tag also destroys preimage resistance: an attacker who wants a message with a "
        "specific tag needs only 2^16 attempts, about 65,000 hashes. Truncation is therefore never "
        "a shortcut for speed. Where a short tag is unavoidable - a checksum, a truncated MAC - "
        "the tag length must be chosen against the birthday bound, not against the preimage bound.",
        bg=HexColor("#E3F2FD"), border=HexColor("#1A237E"), title="Security consequence"))

    # ---------------- Task 2 ----------------
    e.append(Paragraph("Task 2 - Collision Detection on Complete SHA-256", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "<b>Requirement:</b> generate random messages and check for collisions using complete "
        "SHA-256 hashes.", s_body))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "The same search that succeeded in 230 messages at 16 bits is now repeated on the full "
        "256-bit digest. The code is deliberately unchanged apart from the removal of the "
        "truncation, so the experiment isolates one variable: the size of the tag space.", s_body))
    e.append(Spacer(1, 4))
    e.append(KeepTogether([Paragraph("Execution output", s_h2)] +
                          shot("shot_task2.png",
                               "Fig. 3: One million messages hashed with complete SHA-256 - no "
                               "collision - followed by the same search on truncated tags.",
                               max_h=470)))
    e.append(Spacer(1, 4))
    e.append(Paragraph("Implementation (task2_sha256_collision.py)", s_h2))
    e.extend(make_code_blocks(read_code("task2_sha256_collision.py"), 4))
    e.append(Spacer(1, 2))
    e.append(Paragraph(
        "After the main scan the program runs the identical generator with 16-, 24- and 32-bit "
        "tags, several trials each, and reports the mean number of messages needed for the first "
        "collision. This turns a negative result into a measurement: the reader can see the "
        "birthday bound being obeyed at small tag sizes and can then extrapolate to 256 bits.",
        s_body))


    e.append(Paragraph("Result analysis", s_h2))
    e.append(Paragraph(
        "One million distinct messages produced one million distinct digests. The probability of "
        "a collision in that sample is n^2 / 2^257 = 4.3e-66, so the empty result is not luck - it "
        "is the only outcome that was ever possible. To reach a 50 percent chance an attacker "
        "needs 2^128 messages, which at one billion hashes per second would take 1.08e22 years, "
        "roughly a trillion times the age of the universe.", s_body))
    e.append(Spacer(1, 2))
    e.append(make_table(
        ["Tag size", "Tag space", "Messages to first collision", "Birthday bound", "Ratio"],
        [
            ["16 bits", "65,536", "328 (measured, 200 trials)", "321", "1.02x"],
            ["24 bits", "16,777,216", "5,100 (measured, 60 trials)", "5,134", "0.99x"],
            ["32 bits", "4,294,967,296", "99,145 (measured, 15 trials)", "82,137", "1.21x"],
            ["256 bits", "1.16e77", "not reachable", "3.40e38", "-"],
        ],
        [58, 82, 150, 85, CW - 375]))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "Each additional 8 bits of tag multiplied the work by 15.5x and 19.4x respectively, "
        "against a theoretical 16x. The agreement is close enough that the scaling rule can be "
        "trusted: every 8 bits added to a digest multiply the collision search by 2^4. Applied "
        "from 32 bits to 256 bits, that is 28 steps of 16x, or a factor of 2^112 - which is "
        "exactly why the full digest never collides in any experiment that can be run.", s_body))
    e.append(Spacer(1, 4))
    e.append(make_callout(
        "SHA-256 has no known collision. The two published breaks in the SHA-2 family are "
        "theoretical reduced-round results, and the practical collision attacks that exist are "
        "against MD5 (seconds on a laptop) and SHA-1 (about 2^63 work, demonstrated in 2017 with "
        "the SHAttered PDF pair). A lab exercise can therefore only attack SHA-256 by shortening "
        "it, which is what Task 1 does.", title="What has actually been broken"))

    # ---------------- Task 3 ----------------
    e.append(Paragraph("Task 3 - Hash Stretching with PBKDF2-HMAC-SHA256", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "<b>Requirement:</b> implement PBKDF2 using SHA-256 with 1,000, 10,000 and 100,000 "
        "iterations and compare the execution times.", s_body))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "A plain SHA-256 of a password takes under a microsecond, so a single GPU tests around "
        "10^10 candidates per second and the entire six-character alphanumeric space falls in "
        "about a fifth of a second. Stretching does not make the hash stronger; it makes each "
        "guess more expensive by repeating the work. PBKDF2 defines", s_body))
    e.append(Paragraph(
        "U1 = PRF(P, S || INT(i))      Uj = PRF(P, U(j-1))      T = U1 xor U2 xor ... xor Uc",
        S("formula2", font="Courier", size=8.6, color=NAVY, align=TA_CENTER, sa=4, sb=2)))
    e.append(Paragraph(
        "where c is the iteration count. The attacker must perform all c iterations for every "
        "candidate, while the legitimate server performs them once per login. The cost is paid "
        "deliberately, and the iteration count is tuned so that one verification takes a few "
        "hundred milliseconds on the server hardware - slow enough to hurt the attacker, fast "
        "enough not to be a denial of service against the login form.", s_body))
    e.append(Spacer(1, 2))
    for f in shot("diagram_stretching.png",
                  "Fig. 4: Measured cost per derivation and the resulting attacker guess rate. "
                  "A log scale is used because the times span two orders of magnitude.",
                  max_h=205):
        e.append(f)
    e.append(Spacer(1, 2))
    e.append(KeepTogether([Paragraph("Execution output", s_h2)] +
                          shot("shot_task3.png",
                               "Fig. 5: Task 3 run - timing at three iteration counts, the derived "
                               "keys, and the attacker cost table.", max_h=470)))
    e.append(Spacer(1, 4))
    e.append(Paragraph("Implementation (task3_pbkdf2_stretching.py)", s_h2))
    e.extend(make_code_blocks(read_code("task3_pbkdf2_stretching.py"), 4))


    e.append(Paragraph("Result analysis", s_h2))
    e.append(Paragraph(
        "The measured times were 1.36 ms, 14.65 ms and 141.29 ms. The ratios are 10.8x and 104.1x "
        "for a 10x and a 100x increase in iterations, and the per-iteration cost stayed inside a "
        "narrow band of 1.36 to 1.46 microseconds. That flatness is the proof that PBKDF2 is "
        "linear in the work factor: there is no shortcut, no precomputation and no parallelism "
        "inside a single derivation, so the attacker pays exactly the same multiple that the "
        "server pays.", s_body))
    e.append(Spacer(1, 2))
    e.append(make_table(
        ["Iterations", "Measured time", "Cost vs 1,000", "GPU guesses/s", "Exhaust 36^6"],
        [
            ["1,000", "1.36 ms", "1.0x", "10,000,000", "3.6 min"],
            ["10,000", "14.65 ms", "10.8x", "1,000,000", "36.3 min"],
            ["100,000", "141.29 ms", "104.1x", "100,000", "6.05 h"],
        ],
        [72, 88, 78, 108, CW - 346]))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "The last two columns use an attacker with a single high-end GPU at 10^10 SHA-256 "
        "operations per second against a six-character alphanumeric password (36^6 = 2.18e9 "
        "candidates). At 1,000 iterations the whole space falls in under four minutes, so a low "
        "iteration count offers essentially no protection. At 100,000 iterations the same search "
        "takes six hours, and the defender's cost for a legitimate login is still only 141 ms.",
        s_body))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "The three derived keys are all different, which is expected: the iteration count is part "
        "of the input to the key derivation, not a tuning parameter applied afterwards. The stored "
        "record must therefore keep the iteration count next to the salt, otherwise the server "
        "cannot reproduce the key. The final three checks confirm the other two properties - the "
        "same inputs always give the same key, and a different salt gives a completely different "
        "one.", s_body))
    e.append(Spacer(1, 4))
    e.append(make_callout(
        "OWASP recommends 600,000 iterations of PBKDF2-HMAC-SHA256 for password storage, and "
        "RFC 8018 requires at least 1,000. The 100,000 used here is a teaching value that keeps "
        "the lab responsive; it is the shape of the curve, not the specific number, that the "
        "exercise is meant to establish. Argon2id is now preferred over PBKDF2 because it also "
        "demands memory, which removes the GPU advantage that PBKDF2 still allows.",
        bg=HexColor("#FFF8E1"), border=HexColor("#B08800"), title="Practical guidance"))

    # ---------------- Task 4 ----------------
    e.append(Paragraph("Task 4 - Salted Password Hashing and Verification", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "<b>Requirement:</b> hash a password using a random salt and PBKDF2, then verify the "
        "password entered by the user.", s_body))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "Stretching raises the cost of one guess, but it does not stop an attacker from "
        "precomputing. Without a salt, every user who chose the password <i>HashLab@2026</i> has "
        "the same digest, so one table built once cracks all of them. A salt is a random value "
        "generated per password and stored beside the digest in clear. It does not need to be "
        "secret - its only job is to make each stored hash unique, so a table built for one record "
        "is useless for the next one.", s_body))
    e.append(Spacer(1, 2))
    for f in shot("diagram_salt.png",
                  "Fig. 6: Two users with the same password. The random salt forces two different "
                  "derived keys, so the stored records cannot be compared or shared.",
                  max_h=190):
        e.append(f)
    e.append(Spacer(1, 2))
    e.append(KeepTogether([Paragraph("Execution output", s_h2)] +
                          shot("shot_task4.png",
                               "Fig. 7: Task 4 run - registration, successful verification, "
                               "rejection of a wrong password, and salt uniqueness.",
                               max_h=520)))
    e.append(Spacer(1, 4))
    e.append(Paragraph("Implementation (task4_password_salt.py)", s_h2))
    e.extend(make_code_blocks(read_code("task4_password_salt.py"), 4))


    e.append(Paragraph("Result analysis", s_h2))
    e.append(Paragraph(
        "Registration produced a self-describing record: the algorithm name, the iteration count, "
        "the 16-byte salt and the 32-byte derived key, 48 bytes in total. The password itself is "
        "nowhere in the record, and it cannot be recovered from it - the only operation available "
        "to the server is to derive the key again from a candidate password and compare.", s_body))
    e.append(Spacer(1, 2))
    e.append(make_table(
        ["Field", "Size", "Purpose"],
        [
            ["algorithm", "variable", "Names the KDF so the record can be migrated later."],
            ["iterations", "8 bytes", "Work factor. Required to reproduce the key."],
            ["salt", "16 bytes", "Random per password. Makes the digest unique."],
            ["hash", "32 bytes", "PBKDF2 output. Compared in constant time."],
        ],
        [78, 62, CW - 140]))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "The verification step recomputes the key with the stored salt and the stored iteration "
        "count, then compares with <i>hmac.compare_digest</i> rather than the <i>==</i> operator. "
        "A byte-by-byte comparison returns as soon as it finds a mismatch, so its running time "
        "leaks how many leading bytes were correct; an attacker who can time the login endpoint "
        "can recover the digest one byte at a time. The constant-time comparison removes that "
        "channel.", s_body))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "The salt-uniqueness section shows the effect directly. Both records were built from the "
        "same password, yet the salts and the derived keys are completely different, and each "
        "record still verifies its own password. The wrong password was rejected, which confirms "
        "that the comparison is actually being performed and is not accepting everything.", s_body))
    e.append(Spacer(1, 4))
    e.append(make_callout(
        "A salt is public and per-user; a <b>pepper</b> is secret and global. The pepper is kept "
        "in application configuration rather than in the database, so an attacker who steals only "
        "the database cannot even start guessing. The two are complementary: the salt stops "
        "precomputation, the pepper stops offline cracking after a database leak. Neither replaces "
        "the iteration count.", bg=HexColor("#E3F2FD"), border=HexColor("#1A237E"),
        title="Salt and pepper"))
    e.append(Spacer(1, 5))

    # ---------------- Conclusion ----------------
    e.append(Paragraph("Conclusion", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "The four tasks trace one idea from theory to deployment: the security of a hash is "
        "measured by the cheapest attack against it, not by the size of its output. Task 1 showed "
        "that truncating SHA-256 to 16 bits reduces the collision search to about 321 messages, "
        "and the measured mean of 336 over 200 trials matched the birthday bound to within five "
        "percent. Task 2 repeated the identical search on the full digest and found nothing in a "
        "million messages, with a collision probability of 4.3e-66; the comparison at 16, 24 and "
        "32 bits showed the search growing by roughly 16x per 8 bits, exactly as the bound "
        "predicts. Together they establish that SHA-256 is collision resistant at its full length "
        "and that any truncation must be sized against 2^(b/2), not 2^b.", s_body))
    e.append(Spacer(1, 4))
    e.append(Paragraph(
        "Tasks 3 and 4 moved from breaking the primitive to using it correctly. PBKDF2 was shown "
        "to be linear in its iteration count, with a flat cost of about 1.4 microseconds per "
        "iteration, which turned a sub-second exhaustive search into six hours for a six-character "
        "password. Adding a random salt per user then removed the last shortcut available to the "
        "attacker: with a 16-byte salt the precomputation must be repeated for each of 2^128 "
        "possible salts, so a rainbow table stops being an asset and becomes a liability. The "
        "resulting recipe - salted, stretched, constant-time verified, with the parameters stored "
        "alongside the digest - is the minimum acceptable design for password storage.", s_body))
    e.append(Spacer(1, 4))

    e.append(Paragraph("References", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    for i, r in enumerate([
        "NIST FIPS 180-4, <i>Secure Hash Standard (SHS)</i>, National Institute of Standards and "
        "Technology, August 2015.",
        "NIST FIPS 202, <i>SHA-3 Standard: Permutation-Based Hash and Extendable-Output "
        "Functions</i>, 2015.",
        "B. Kaliski, <i>RFC 2898 / PKCS #5: Password-Based Cryptography Specification v2.0</i>, "
        "IETF, 2000.",
        "K. Moriarty, B. Kaliski, A. Rusch, <i>RFC 8018: PKCS #5 v2.1 - Password-Based "
        "Cryptography Specification</i>, IETF, 2017.",
        "W. Stallings, <i>Cryptography and Network Security: Principles and Practice</i>, 7th ed., "
        "Pearson, chapters 11 and 12.",
        "A. J. Menezes, P. C. van Oorschot, S. A. Vanstone, <i>Handbook of Applied Cryptography</i>, "
        "CRC Press, chapter 9 (Hash functions and the birthday attack).",
        "OWASP Foundation, <i>Password Storage Cheat Sheet</i>, 2023.",
        "Python Standard Library, <i>hashlib - Secure hashes and message digests</i>, "
        "https://docs.python.org/3/library/hashlib.html",
    ], 1):
        e.append(Paragraph(f"[{i}] {r}", S(f"ref{i}", size=8.6, color=TD, sa=2, leading=11, li=16)))

    doc = SimpleDocTemplate(OUT_PDF, pagesize=A4, leftMargin=LM, rightMargin=RM,
                            topMargin=TM, bottomMargin=BM,
                            title="Information Security Lab Manual 06 - Secure Hash Functions",
                            author="M.Fezan (Fall-23-BSCS-466)")
    doc.build(e, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print("DONE:", OUT_PDF)


if __name__ == "__main__":
    build()
