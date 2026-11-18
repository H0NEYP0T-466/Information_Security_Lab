#!/usr/bin/env python3
"""
Information Security Lab - Lab Manual 07 Generator
Author: Muhammad Fezan (Fall-23-BSCS-466)
Instructor: Sir Mukkaram Ahmad (Asst. Lect.)
Course: Information Security Lab (7th Semester - Fall 2026)
Topic: Blockchain Technology - Mining Rewards, Miner Wallets, Block Creation,
       Peer-to-Peer (P2P) Network Architecture & Multi-Node Synchronization.
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
G  = HexColor("#1B5E20")       # Primary Forest Green
LG = HexColor("#E8F5E9")       # Light Green Background
AG = HexColor("#2E7D32")       # Accent Green
TD = HexColor("#212121")       # Dark Charcoal Text
SG = HexColor("#555555")       # Subtitle Grey
FG = HexColor("#777777")       # Footer Grey
BG_CODE = HexColor("#F8F9FA")  # Code Box Background
BORDER_CODE = HexColor("#CFD8DC") # Code Box Border
NAVY = HexColor("#1A237E")     # Accent Navy Blue

PAGE_W, PAGE_H = A4
LM = RM = TM = BM = 1 * inch
CW = PAGE_W - LM - RM
SB_W = 12 * mm

LAB_DIR = "/home/honeypot/Univeristy_Data/IS(L)/LAB 7"
SOL_DIR = os.path.join(LAB_DIR, "solution")
SHOT_DIR = os.path.join(SOL_DIR, "shots")
LOGO_PATH = "/home/honeypot/.hermes/skills/lgu-assignment/assets/lgu-logo.png"
OUT_PDF = os.path.join(LAB_DIR, "Information_Security_Lab_Manual_07.pdf")

RUNNING_HEAD = ("Information Security Lab  |  Lab Manual 07  -  Blockchain "
                "Technology, Mining Rewards & P2P Synchronization")


def S(name, font="Times-Roman", size=12, color=TD, align=TA_LEFT,
      bold=False, italic=False, sa=4, sb=0, li=0, leading=None):
    fname = "Times-Bold" if bold else ("Times-Italic" if italic else font)
    return ParagraphStyle(name, fontName=fname, fontSize=size, textColor=color,
                          alignment=align, spaceAfter=sa, spaceBefore=sb,
                          leading=leading or (size * 1.3), leftIndent=li)


s_ct = S("ct", size=10, color=G, align=TA_CENTER, bold=True, sa=3)
s_ctt = S("ctt", size=17, color=G, align=TA_CENTER, bold=True, sa=4)
s_cs = S("cs", size=10.2, color=SG, align=TA_CENTER, italic=True, sa=6)
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

code_style = ParagraphStyle("CodeStyle", fontName="Courier", fontSize=6.2,
                            leading=7.4, textColor=NAVY)


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
    items.append(Paragraph("LAB MANUAL # 7", s_ctt))
    items.append(Paragraph("Blockchain Technology: Mining Rewards, Miner Wallets, "
                           "Proof-of-Work &amp; Peer-to-Peer (P2P) Network Synchronization", s_cs))
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
        [Paragraph("<b>CONTEXT:</b>", s_cl), Paragraph("Lab Manual # 7 - Blockchain Technology (Week 07 task sheet)", s_cv)],
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
# CONTENT GENERATOR
# ======================================================================
def build():
    e = build_cover()

    # ---------------- Overview ----------------
    e.append(Paragraph("Lab 07 - Objectives and Scope", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "A blockchain is a cryptographically secured, append-only distributed ledger operated "
        "across a decentralized network of autonomous peer nodes without reliance on a central "
        "clearinghouse. Trust in such an open environment cannot depend on administrative authority; "
        "instead, it is sustained through two foundational pillars: <b>economic incentive design</b> "
        "(mining rewards that compensate participants for expending computational work to validate and "
        "order blocks) and <b>decentralized consensus synchronization</b> (protocols that enable "
        "independent nodes to converge deterministically onto a single, canonical truth despite network "
        "latency and untrusted peers). This laboratory investigates both mechanisms by implementing an "
        "end-to-end blockchain simulation from first principles in Python.", s_body))
    e.append(Spacer(1, 2))
    e.append(Paragraph("Learning outcomes (CLO 4 / GA 3 / BT Level C4):", s_h2))
    for t in [
        "Explain the role of the coinbase mining reward (50 coins) in incentivizing honest hash-power and maintaining network security.",
        "Maintain decentralized miner wallet states and enforce state transition invariants across sequential block creation.",
        "Implement cryptographic SHA-256 block hashing and Proof-of-Work nonce discovery to establish tamper-evident block linkages.",
        "Architect autonomous peer nodes that maintain private, isolated copies of the distributed blockchain ledger.",
        "Implement peer-to-peer (P2P) synchronization governed by the Longest Chain Rule (Nakamoto Consensus) to achieve global ledger convergence.",
        "Verify multi-node state consistency, cryptographic integrity, and fork resolution under dynamic mining events.",
    ]:
        e.append(Paragraph(f"&bull; {t}", s_bul))
    e.append(Spacer(1, 4))

    e.append(make_callout(
        "<b>Environment & Tooling:</b> Python 3.11 with the standard <i>hashlib</i>, <i>json</i>, "
        "<i>time</i>, and <i>copy</i> modules executed inside the Hermes virtual environment at "
        "/home/honeypot/.hermes/hermes-agent/venv. Cryptographic digests adhere to NIST FIPS 180-4 "
        "SHA-256. Terminal outputs are executed in real time, captured verbatim, and rendered into "
        "high-fidelity graphical artifacts via Pillow before ReportLab PDF compilation.",
        title="Execution Environment"))
    e.append(Spacer(1, 4))

    # ---------------- Theory ----------------
    e.append(Paragraph("1. Theoretical Foundations of Blockchain Systems", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "A blockchain organizes state transitions into ordered containers called <b>blocks</b>. "
        "Each block encapsulates a header and a body. The header includes the index, Unix timestamp, "
        "a cryptographic pointer (<i>previous_hash</i>) referencing the SHA-256 digest of the immediate "
        "ancestor, and an arbitrary counter termed the <b>nonce</b>. Because every block's hash incorporates "
        "the previous block's hash, any retrofitted alteration to an earlier block invalidates the "
        "cryptographic hashes of all descendant blocks, producing an immutable, tamper-evident hash chain.",
        s_body))
    e.append(Spacer(1, 2))

    e.append(make_table(
        ["Component", "Functional Definition", "Security Guarantee"],
        [
            ["Genesis Block", "The hardcoded initial block (index 0) with previous_hash = 0^64.",
             "Forms the immutable root of trust for all participating nodes."],
            ["Proof-of-Work (PoW)", "Mathematical puzzle requiring hash to fall below target (e.g. prefix '00').",
             "Imposes thermodynamic computational cost, preventing costless spam and Sybil attacks."],
            ["Mining Reward", "Minting of unbacked protocol tokens (50 coins) credited to block miner.",
             "Aligns individual self-interest with collective security and rules enforcement."],
            ["Peer Node", "Autonomous network daemon maintaining a local, isolated ledger instance.",
             "Eliminates single points of failure (SPOF) and censorship bottlenecks."],
            ["Nakamoto Consensus", "Acceptance of the longest cryptographically valid chain across peers.",
             "Guarantees eventual consistency and deterministic fork resolution across latency."],
        ],
        [100, 200, CW - 300]))
    e.append(Spacer(1, 4))

    e.append(Paragraph("1.1 The Mining Reward Mechanism and State Transitions", s_h2))
    e.append(Paragraph(
        "In a decentralized ledger, there is no centralized treasury to pay validators. Instead, the protocol "
        "defines an inflationary subsidy known as the <b>coinbase reward</b>. When a miner succeeds in finding "
        "a valid nonce that satisfies the network difficulty target, the block includes a designated reward transaction "
        "crediting 50 new coins to the miner's public address. This design ensures that miners have a positive "
        "financial incentive to expend electricity and computational power on extending the legitimate chain rather than "
        "attempting double-spending reorganizations.", s_body))
    e.append(Spacer(1, 2))

    for f in shot("diagram_mining_reward.png",
                  "Fig. 1: Architectural pipeline of a block creation and mining reward state transition. "
                  "The coinbase payload (+50 coins) is bound into the block header, hashed via SHA-256, and "
                  "credited to the miner's wallet upon block finalization.", max_h=230):
        e.append(f)

    e.append(Paragraph("1.2 Decentralized P2P Gossip and Nakamoto Consensus", s_h2))
    e.append(Paragraph(
        "In a Peer-to-Peer (P2P) topology, nodes do not share memory or master clocks. When Node1 discovers a new block, "
        "it broadcasts the block to its neighbors (Node2 and Node3). Upon receipt, each recipient executes two strict checks: "
        "(1) <b>Cryptographic Verification:</b> every block's internal hash must match its payload, link to its predecessor, "
        "and satisfy the Proof-of-Work difficulty; (2) <b>Longest Chain Selection:</b> if the incoming valid chain is longer "
        "than the node's local chain, the node reorganizes its local state to match the peer's branch. This guarantees that "
        "disparate network nodes converge reliably onto the canonical history containing the greatest cumulative proof of work.",
        s_body))
    e.append(Spacer(1, 2))

    for f in shot("diagram_p2p_sync.png",
                  "Fig. 2: Multi-node peer-to-peer network mesh and block propagation. Node1 mines Block #1 and propagates "
                  "it across the network; Node2 and Node3 adopt the longer valid branch via sync_with_node().",
                  max_h=240):
        e.append(f)

    e.append(PageBreak())

    # ---------------- Task 1 ----------------
    e.append(Paragraph("Task 1 - Simplified Blockchain Mining Reward System", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "<b>Requirement:</b> Create a <i>Blockchain</i> class initialized with a Genesis block. Set the mining "
        "reward to 50 coins. Implement a <i>mine_block(miner_address)</i> method that binds reward information "
        "into the new block, computes proof-of-work, and credits 50 coins to the miner's wallet. Implement "
        "<i>print_rewards()</i> to display the earned rewards of all miners. Test the program by mining blocks "
        "for at least two distinct miner addresses.", s_body))
    e.append(Spacer(1, 4))

    e.append(KeepTogether([Paragraph("Execution Output (Task 1)", s_h2)] +
                          shot("shot_task1.png",
                               "Fig. 3: Real terminal execution output of task1_mining_rewards.py demonstrating "
                               "Genesis block initialization, sequential mining by multiple miners (Alice, Bob, Fezan), "
                               "automatic wallet balance crediting, and cryptographic chain verification.",
                               max_h=520)))
    e.append(Spacer(1, 4))

    e.append(Paragraph("Implementation (task1_mining_rewards.py)", s_h2))
    e.extend(make_code_blocks(read_code("task1_mining_rewards.py"), 3))
    e.append(Spacer(1, 2))

    e.append(Paragraph("Task 1 Results and Technical Analysis", s_h2))
    e.append(Paragraph(
        "The implementation initializes the blockchain with a hardcoded Genesis block at index 0. Four consecutive "
        "blocks are mined across three distinct miner identities: <i>0x71A4_Alice_Miner</i> (mined Blocks #1 and #3), "
        "<i>0x94B2_Bob_Miner</i> (mined Block #2), and <i>0x466F_Fezan_Miner</i> (mined Block #4). Each block includes "
        "the coinbase transaction structure in its payload and computes a valid SHA-256 hash satisfying the difficulty "
        "target of two leading zeros (e.g. Block #1 hash <i>000bc78e...</i>, Block #2 hash <i>00d057de...</i>).",
        s_body))
    e.append(Spacer(1, 2))
    e.append(Paragraph(
        "The wallet ledger confirms precise balance accumulation: Alice receives 100.00 coins (2 blocks &times; 50), "
        "Bob receives 50.00 coins (1 block &times; 50), and Fezan receives 50.00 coins (1 block &times; 50), yielding a total "
        "distributed currency volume of 200.00 coins across 4 mined blocks. Calling <i>is_chain_valid()</i> confirms that "
        "all 5 blocks (Genesis + 4 mined) strictly adhere to cryptographic hash chaining and proof-of-work invariants.",
        s_body))
    e.append(Spacer(1, 4))

    e.append(PageBreak())

    # ---------------- Task 2 ----------------
    e.append(Paragraph("Task 2 - Basic Blockchain Peer-to-Peer (P2P) Network Simulation", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "<b>Requirement:</b> Create an autonomous <i>Node</i> class accepting a node name, where each node maintains "
        "its own independent copy of the blockchain. Instantiate at least three nodes (Node1, Node2, and Node3). "
        "Implement a <i>sync_with_node()</i> method to synchronize ledgers between peers using consensus rules. "
        "Mine a new block on Node1, synchronize Node2 and Node3 with Node1, display the blockchain of each node, "
        "and verify that all three nodes contain the exact same number of blocks and identical state.", s_body))
    e.append(Spacer(1, 4))

    e.append(KeepTogether([Paragraph("Execution Output (Task 2)", s_h2)] +
                          shot("shot_task2.png",
                               "Fig. 4: Terminal execution output of task2_p2p_network.py demonstrating multi-node "
                               "initialization, out-of-sync detection, peer synchronization via Nakamoto Consensus, "
                               "and complete convergence verification across Node1, Node2, and Node3.",
                               max_h=520)))
    e.append(Spacer(1, 4))

    e.append(Paragraph("Implementation (task2_p2p_network.py)", s_h2))
    e.extend(make_code_blocks(read_code("task2_p2p_network.py"), 3))
    e.append(Spacer(1, 2))

    e.append(Paragraph("Task 2 Results and Consensus Verification", s_h2))
    e.append(Paragraph(
        "Task 2 models true decentralized operation by ensuring that each Node instance owns a decoupled, deep-copied "
        "ledger. In Step 1, Node1, Node2, and Node3 each initialize with a Genesis block (height = 1). When Node1 mines "
        "Block #1, its local ledger advances to length 2, while Node2 and Node3 remain at length 1, creating an intentional "
        "temporary state divergence.", s_body))
    e.append(Spacer(1, 2))
    e.append(Paragraph(
        "Executing <i>Node2.sync_with_node(Node1)</i> and <i>Node3.sync_with_node(Node1)</i> triggers the Nakamoto Consensus "
        "routine: each peer validates that Node1's chain has unbroken SHA-256 linkages and valid proof-of-work hashes, and "
        "recognizes that length 2 is strictly greater than local length 1. Both peers adopt the longer chain. The verification "
        "matrix confirms 100% agreement: all three nodes hold exactly 2 blocks with the identical tip hash <i>0099faae50f9f7...</i>.",
        s_body))
    e.append(Spacer(1, 2))
    e.append(Paragraph(
        "To test network resilience beyond unidirectional broadcast, an advanced second round is simulated: Node2 mines "
        "Block #2 (height = 3), and peers Node1 and Node3 synchronize with Node2. Once again, all nodes seamlessly adopt "
        "the newly extended chain, concluding with length = 3 and identical tip hash <i>0049ceeba25601...</i> across the entire mesh.",
        s_body))
    e.append(Spacer(1, 4))

    # ---------------- Submission Script Overview ----------------
    e.append(Paragraph("3. Unified Submission Script (RollNo_Blockchain_HomeTask6-7.py)", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "To strictly fulfill the file naming and delivery specifications set forth in the Week 07 assignment sheet "
        "(<i>File Name: RollNo_Blockchain_HomeTask6-7.py</i>), a unified standalone script named "
        "<b>Fall-23-BSCS-466_Blockchain_HomeTask6-7.py</b> was authored. It integrates both Task 1 and Task 2 into a single, "
        "fully encapsulated executable with zero external dependencies beyond the Python standard library.", s_body))
    e.append(Spacer(1, 2))

    e.append(make_table(
        ["Requirement Dimension", "Task 1 Specification", "Task 2 Specification", "Unified Script Status"],
        [
            ["Class Architecture", "Blockchain, Block, Wallets", "Node, Blockchain, Block", "Fully Modular Object Model"],
            ["Mining Reward", "50 coins per mined block", "Preserved across block additions", "Verified: 50.0 coins constant"],
            ["Cryptographic Security", "SHA-256 + PoW difficulty = 2", "SHA-256 + PoW + Chain Validation", "Strict FIPS 180-4 Compliance"],
            ["P2P Network Topology", "Single node ledger testing", "Tri-node mesh (Node1, Node2, Node3)", "3 Autonomous Node Instances"],
            ["Consensus Rule", "Single branch extension", "Longest Valid Chain (Nakamoto)", "100% Hash Convergence Passed"],
        ],
        [110, 120, 125, CW - 355]))
    e.append(Spacer(1, 4))

    # ---------------- Conclusion ----------------
    e.append(Paragraph("Conclusion", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    e.append(Paragraph(
        "This laboratory successfully demonstrated the mechanics of decentralized trust, mining incentive structures, and "
        "peer-to-peer consensus in blockchain technology. Task 1 established that the coinbase reward mechanism provides "
        "the necessary economic game theory to motivate computational investment, demonstrating that wallet state tracking "
        "remains deterministic and verifiable as new blocks are mined and cryptographically bound to the ledger.", s_body))
    e.append(Spacer(1, 3))
    e.append(Paragraph(
        "Task 2 demonstrated how decentralized autonomous nodes maintain localized replicas of the global state and converge "
        "deterministically via the Longest Chain Rule. By validating proof-of-work hashes before adopting peer branches, the "
        "network protects itself against invalid blocks, sybil spoofing, and transaction forgery, ensuring eventual consistency "
        "without a central coordinator. Together, both tasks reinforce the core information security principles that underpin "
        "modern decentralized ledgers.", s_body))
    e.append(Spacer(1, 4))

    # ---------------- References ----------------
    e.append(Paragraph("References", s_h1))
    e.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    for i, r in enumerate([
        "S. Nakamoto, <i>Bitcoin: A Peer-to-Peer Electronic Cash System</i>, 2008. https://bitcoin.org/bitcoin.pdf",
        "A. M. Antonopoulos, <i>Mastering Bitcoin: Programming the Open Blockchain</i>, 2nd ed., O'Reilly Media, 2017.",
        "NIST FIPS 180-4, <i>Secure Hash Standard (SHS)</i>, National Institute of Standards and Technology, August 2015.",
        "A. Narayanan, J. Bonneau, E. Felten, A. Miller, S. Goldfeder, <i>Bitcoin and Cryptocurrency Technologies</i>, Princeton University Press, 2016.",
        "A. S. Tanenbaum, M. van Steen, <i>Distributed Systems: Principles and Paradigms</i>, 3rd ed., CreateSpace, 2017.",
        "Python Software Foundation, <i>hashlib - Secure hashes and message digests</i>, Python 3.11 Documentation, 2026.",
    ], 1):
        e.append(Paragraph(f"[{i}] {r}", S(f"ref{i}", size=8.6, color=TD, sa=2, leading=11, li=16)))

    doc = SimpleDocTemplate(OUT_PDF, pagesize=A4, leftMargin=LM, rightMargin=RM,
                            topMargin=TM, bottomMargin=BM,
                            title="Information Security Lab Manual 07 - Blockchain Technology",
                            author="M.Fezan (Fall-23-BSCS-466)")
    doc.build(e, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print("DONE:", OUT_PDF)


if __name__ == "__main__":
    build()
