#!/usr/bin/env python3
"""
Populate Information_Security_Lab_OEL.docx with:
1. Question typed first
2. Python Code implementation (formatted in-document code box)
3. Genuine Linux terminal window screenshot showing execution output (no code in screenshot)
Author: Muhammad Fezan (Fall-23-BSCS-466)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DOCX_OUT = "/home/honeypot/Downloads/Documents/Information_Security_Lab_OEL.docx"
DOCX_LOCAL = "/home/honeypot/Univeristy_Data/IS(L)/OEL/Information_Security_Lab_OEL.docx"
SHOTS_DIR = "/home/honeypot/Univeristy_Data/IS(L)/OEL/solution/shots"


def add_code_block(doc, code_str):
    """Adds a clean, styled code block table in the Word document."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.2)

    # Background color and left border
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8F9FA"/>')
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="CFD8DC"/>'
        f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="1B5E20"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CFD8DC"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="CFD8DC"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(shd)
    tcPr.append(borders)

    # Inner cell padding
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="100" w:type="dxa"/><w:bottom w:w="100" w:type="dxa"/><w:left w:w="140" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(9.5)
    r = p.add_run(code_str.strip("\n"))
    r.font.name = "Consolas"
    r.font.size = Pt(8.0)
    r.font.color.rgb = RGBColor(26, 35, 126)  # Navy Blue


def rebuild_document():
    doc = docx.Document(DOCX_OUT)
    body = doc._element.body

    # 1. Cleanly strip all residual elements after the 7-row Rubrics table
    rubrics_tbl_el = None
    for child in list(body):
        if child.tag.endswith("tbl") and len(child) == 7:
            rubrics_tbl_el = child
            break

    found_rubrics = False
    to_remove = []
    for child in list(body):
        if child == rubrics_tbl_el:
            found_rubrics = True
            continue
        if found_rubrics and not child.tag.endswith("sectPr"):
            to_remove.append(child)

    for el in to_remove:
        body.remove(el)

    primary_color = RGBColor(27, 94, 32)
    charcoal = RGBColor(33, 33, 33)

    # 2. Format header paragraphs
    for p in doc.paragraphs:
        if "Instructor Name:" in p.text:
            p.text = "Instructor Name: Mukkaram Ahmad Khan                                    Program/Semester: BSCS 7th (Sec L)"
            p.runs[0].font.name = "Calibri"
            p.runs[0].font.size = Pt(10)
            p.runs[0].font.bold = True
        elif "Course Code: CC6306" in p.text and "Student Name:" not in p.text:
            p.text = "Course Code: CC6306                  Course Title: Information Security (Lab)            Marks: 10"
            p.runs[0].font.name = "Calibri"
            p.runs[0].font.size = Pt(10)
            p.runs[0].font.bold = True
        elif "Student Name: Muhammad Fezan" in p.text:
            p.text = "Student Name: Muhammad Fezan         Roll Number: Fall-23-BSCS-466"
            p.runs[0].font.name = "Calibri"
            p.runs[0].font.size = Pt(10)
            p.runs[0].font.bold = True
            p.runs[0].font.color.rgb = primary_color

    # Add page break after rubrics
    doc.add_page_break()

    # 3. Task definitions
    tasks = [
        {
            "num": "Question 1: Block Structure & Proof of Work (PoW) Mining Mechanism",
            "spec": "Problem Statement / Instructions:\n"
                    "Implement Block and Blockchain classes in Python using SHA-256 cryptographic hashing. Incorporate a "
                    "Proof of Work (PoW) mining mechanism via compute_proof_of_work() that iteratively increments a nonce "
                    "until the block hash matches a configurable leading-zero difficulty target (difficulty = 2). Link each "
                    "block via previous_hash to maintain an immutable ledger.",
            "code": """class Block:
    def __init__(self, index: int, timestamp: float, data: Any, previous_hash: str = "", nonce: int = 0):
        self.index: int = index
        self.timestamp: float = timestamp
        self.data: Any = data
        self.previous_hash: str = previous_hash
        self.nonce: int = nonce
        self.hash: str = self.compute_hash()

    def compute_hash(self) -> str:
        header = {"index": self.index, "timestamp": self.timestamp, "data": self.data,
                  "previous_hash": self.previous_hash, "nonce": self.nonce}
        return hashlib.sha256(json.dumps(header, sort_keys=True).encode()).hexdigest()

    def compute_proof_of_work(self, difficulty: int) -> int:
        target_prefix = "0" * difficulty
        iterations = 0
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.compute_hash()
            iterations += 1
        return iterations""",
            "img": "shot_q1_terminal.png",
            "caption": "Screenshot 1: Actual terminal output showing block creation and Proof-of-Work mining with difficulty = 2."
        },
        {
            "num": "Question 2: Cryptographic Chain Validation (is_chain_valid)",
            "spec": "Problem Statement / Instructions:\n"
                    "Implement a robust chain validation mechanism is_chain_valid() to verify cryptographic hash integrity "
                    "and previous_hash linkage across all blocks. Ensure both stored hash recomputation and difficulty "
                    "criteria are rigorously checked.",
            "code": """class Blockchain:
    def is_chain_valid(self, verbose: bool = True) -> Tuple[bool, str]:
        target_prefix = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Stored Hash Recomputation Verification
            if current.hash != current.compute_hash():
                return False, f"Hash Mismatch at Block #{current.index}"

            # 2. Cryptographic Linkage Pointer Verification
            if current.previous_hash != previous.hash:
                return False, f"Linkage Broken at Block #{current.index}"

            # 3. Proof-of-Work Target Criterion Verification
            if not current.hash.startswith(target_prefix):
                return False, f"PoW Invalidation at Block #{current.index}"

        return True, "Valid" """,
            "img": "shot_q2_terminal.png",
            "caption": "Screenshot 2: Actual terminal output verifying stored hash recomputation, linkage, and PoW integrity."
        },
        {
            "num": "Question 3: Evaluating Blockchain Immutability via Unauthorized Data Tampering",
            "spec": "Problem Statement / Instructions:\n"
                    "Evaluate blockchain immutability by simulating unauthorized data tampering on an existing block. Modify "
                    "the data payload of an earlier block and run is_chain_valid() to demonstrate that tampering is immediately "
                    "detected and rejected.",
            "code": """# Simulate Unauthorized Data Tampering on Block #1
target_block = blockchain.chain[1]
print(f"Original Block #1 Data : '{target_block.data}'")
print(f"Original Block #1 Hash : '{target_block.hash}'")

# Adversary alters transaction payload in-place
target_block.data = "Alice transfers 100.0 BTC to Hacker"

# Audit blockchain integrity post-tampering
valid, status = blockchain.is_chain_valid(verbose=True)
print(f"Validation Result       : {valid} (Tampering Successfully Detected!)")""",
            "img": "shot_q3_terminal.png",
            "caption": "Screenshot 3: Actual terminal output demonstrating instant tampering detection and validation failure (False)."
        },
        {
            "num": "Question 4: Simulating 51% Majority Attack (Downstream Hash Recalculation)",
            "spec": "Problem Statement / Instructions:\n"
                    "Demonstrate a 51% majority attack where an adversary possessing majority network hash-power recalculates "
                    "the proof-of-work and hashes for the tampered block and all subsequent/downstream blocks to bypass validation, "
                    "and observe the security implications.",
            "code": """# Simulating 51% Majority Attack: Recalculate PoW for all downstream blocks
for i in range(1, len(blockchain.chain)):
    curr_b = blockchain.chain[i]
    prev_b = blockchain.chain[i - 1]
    curr_b.previous_hash = prev_b.hash
    curr_b.nonce = 0
    curr_b.hash = curr_b.compute_hash()
    curr_b.compute_proof_of_work(blockchain.difficulty)

# Re-audit blockchain state post-51% recalculation
valid, status = blockchain.is_chain_valid(verbose=True)
print(f"Validation Result       : {valid} ({status})")""",
            "img": "shot_q4_terminal.png",
            "caption": "Screenshot 4: Actual terminal output showing downstream PoW recalculation bypassing validation (True)."
        }
    ]

    for idx, task in enumerate(tasks):
        # Heading
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(4)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(task["num"])
        r.font.name = "Calibri"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = primary_color

        # Spec
        p_spec = doc.add_paragraph()
        p_spec.paragraph_format.space_before = Pt(0)
        p_spec.paragraph_format.space_after = Pt(2)
        r_spec = p_spec.add_run(task["spec"])
        r_spec.font.name = "Calibri"
        r_spec.font.size = Pt(8.5)
        r_spec.font.italic = True
        r_spec.font.color.rgb = RGBColor(70, 70, 70)

        # Code Block Label
        p_code_lbl = doc.add_paragraph()
        p_code_lbl.paragraph_format.space_before = Pt(2)
        p_code_lbl.paragraph_format.space_after = Pt(1)
        r_code_lbl = p_code_lbl.add_run("Python Source Code:")
        r_code_lbl.font.name = "Calibri"
        r_code_lbl.font.size = Pt(9.0)
        r_code_lbl.font.bold = True
        r_code_lbl.font.color.rgb = primary_color

        # Formatted Code Block
        add_code_block(doc, task["code"])

        # Output Screenshot Header
        p_out_lbl = doc.add_paragraph()
        p_out_lbl.paragraph_format.space_before = Pt(3)
        p_out_lbl.paragraph_format.space_after = Pt(1)
        r_out_lbl = p_out_lbl.add_run("Terminal Execution Output:")
        r_out_lbl.font.name = "Calibri"
        r_out_lbl.font.size = Pt(9.0)
        r_out_lbl.font.bold = True
        r_out_lbl.font.color.rgb = primary_color

        # Terminal Screenshot (Pure Terminal Window)
        img_path = os.path.join(SHOTS_DIR, task["img"])
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.paragraph_format.space_before = Pt(1)
            p_img.paragraph_format.space_after = Pt(1)
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(6.2))

            # Caption
            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.space_before = Pt(1)
            p_cap.paragraph_format.space_after = Pt(4)
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(task["caption"])
            r_cap.font.name = "Calibri"
            r_cap.font.size = Pt(8.0)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(90, 90, 90)

        if idx < len(tasks) - 1:
            doc.add_page_break()

    doc.save(DOCX_OUT)
    doc.save(DOCX_LOCAL)
    print("Cleanly rebuilt DOCX:", DOCX_OUT)


if __name__ == "__main__":
    rebuild_document()
