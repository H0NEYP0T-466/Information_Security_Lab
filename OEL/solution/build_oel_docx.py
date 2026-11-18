#!/usr/bin/env python3
"""
Cleanly rebuild Information_Security_Lab_OEL.docx and export to PDF.
Author: Muhammad Fezan (Fall-23-BSCS-466)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOCX_OUT = "/home/honeypot/Downloads/Documents/Information_Security_Lab_OEL.docx"
DOCX_LOCAL = "/home/honeypot/Univeristy_Data/IS(L)/OEL/Information_Security_Lab_OEL.docx"
SHOTS_DIR = "/home/honeypot/Univeristy_Data/IS(L)/OEL/solution/shots"


def rebuild():
    doc = docx.Document(DOCX_OUT)
    body = doc._element.body

    # Remove all elements after child 15 (which is the rubrics table)
    # Collect elements to remove
    to_remove = []
    found_table_count = 0
    for child in list(body):
        tag = child.tag.split("}")[-1]
        if tag == "tbl":
            found_table_count += 1
            if found_table_count == 2:
                # This is the rubrics table; everything after this needs removal
                continue
        elif found_table_count >= 2 and tag != "sectPr":
            to_remove.append(child)

    for el in to_remove:
        body.remove(el)

    # Clean up top paragraphs
    # Paragraph 3: Instructor info
    # Paragraph 4 & 5: Course code & student info
    primary_color = RGBColor(27, 94, 32)
    charcoal = RGBColor(33, 33, 33)

    p_list = doc.paragraphs
    for i, p in enumerate(p_list):
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

    # Add page break after rubrics table
    doc.add_page_break()

    tasks = [
        {
            "num": "Question 1: Block Structure & Proof of Work (PoW) Mining Mechanism",
            "spec": "Problem Statement / Instructions:\n"
                    "Implement Block and Blockchain classes in Python using SHA-256 cryptographic hashing. Incorporate a "
                    "Proof of Work (PoW) mining mechanism via compute_proof_of_work() that iteratively increments a nonce "
                    "until the block hash matches a configurable leading-zero difficulty target (difficulty = 2). Link each "
                    "block via previous_hash to maintain an immutable ledger.",
            "desc": "Implementation & Verification Summary:\n"
                    "• Block Header: Deterministic JSON serialization ensures consistent SHA-256 hash generation across runs.\n"
                    "• Proof-of-Work: compute_proof_of_work() increments the nonce counter until hash.startswith('0' * difficulty).\n"
                    "• Execution: Successfully mined Genesis Block, Block #1 (nonce: 14), Block #2 (nonce: 364), and Block #3 (nonce: 9).",
            "img": "shot_q1_block_pow.png",
            "caption": "Screenshot 1: Block Class implementation & compute_proof_of_work() mining alongside real terminal execution output."
        },
        {
            "num": "Question 2: Cryptographic Chain Validation (is_chain_valid)",
            "spec": "Problem Statement / Instructions:\n"
                    "Implement a robust chain validation mechanism is_chain_valid() to verify cryptographic hash integrity "
                    "and previous_hash linkage across all blocks. Ensure both stored hash recomputation and difficulty "
                    "criteria are rigorously checked.",
            "desc": "Implementation & Verification Summary:\n"
                    "• Hash Recomputation: Checks current.hash == current.compute_hash() for every block to catch data alterations.\n"
                    "• Linkage Verification: Checks current.previous_hash == previous.hash to ensure chain continuity.\n"
                    "• Difficulty Verification: Checks current.hash.startswith('0' * difficulty) to ensure valid proof-of-work.\n"
                    "• Execution: Initial audit returns True (Valid) across all blocks with 100% agreement.",
            "img": "shot_q2_chain_validation.png",
            "caption": "Screenshot 2: is_chain_valid() implementation verifying hash recomputation, linkage, and PoW, returning True."
        },
        {
            "num": "Question 3: Evaluating Blockchain Immutability via Unauthorized Data Tampering",
            "spec": "Problem Statement / Instructions:\n"
                    "Evaluate blockchain immutability by simulating unauthorized data tampering on an existing block. Modify "
                    "the data payload of an earlier block and run is_chain_valid() to demonstrate that tampering is immediately "
                    "detected and rejected.",
            "desc": "Implementation & Verification Summary:\n"
                    "• Tampering Action: Attacker alters Block #1 payload from 'Alice transfers 10.0 BTC to Bob' to 'Alice transfers 100.0 BTC to Hacker'.\n"
                    "• Detection: is_chain_valid() flags stored hash ('00821e..') mismatch against recomputed hash ('4ffffb..').\n"
                    "• Output: Validation returns False (Tampering Successfully Detected!), proving tamper-evidence.",
            "img": "shot_q3_tampering_simulation.png",
            "caption": "Screenshot 3: Unauthorized data tampering on Block #1 triggering hash mismatch and validation failure (False)."
        },
        {
            "num": "Question 4: Simulating 51% Majority Attack (Downstream Hash Recalculation)",
            "spec": "Problem Statement / Instructions:\n"
                    "Demonstrate a 51% majority attack where an adversary possessing majority network hash-power recalculates "
                    "the proof-of-work and hashes for the tampered block and all subsequent/downstream blocks to bypass validation, "
                    "and observe the security implications.",
            "desc": "Implementation & Verification Summary:\n"
                    "• Downstream Recalculation: Attacker recalculates Block #1 PoW -> updates Block #2 previous_hash -> recalculates "
                    "Block #2 PoW -> updates Block #3 previous_hash -> recalculates Block #3 PoW.\n"
                    "• Bypass: is_chain_valid() returns True (Valid) because all hashes, links, and difficulties match on this branch.\n"
                    "• Security Implication: Demonstrates why decentralized consensus (majority voting / longest chain rule) is "
                    "essential: an attacker with >50% hash power can outpace honest nodes and force peers to accept a modified history.",
            "img": "shot_q4_51_percent_attack.png",
            "caption": "Screenshot 4: 51% attack recalculating downstream proof-of-work hashes, restoring internal validity (True)."
        }
    ]

    for idx, task in enumerate(tasks):
        # Heading
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(6)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(task["num"])
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = primary_color

        # Spec
        p_spec = doc.add_paragraph()
        p_spec.paragraph_format.space_before = Pt(0)
        p_spec.paragraph_format.space_after = Pt(2)
        r_spec = p_spec.add_run(task["spec"])
        r_spec.font.name = "Calibri"
        r_spec.font.size = Pt(9.5)
        r_spec.font.italic = True
        r_spec.font.color.rgb = RGBColor(60, 60, 60)

        # Desc
        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.space_before = Pt(0)
        p_desc.paragraph_format.space_after = Pt(4)
        r_desc = p_desc.add_run(task["desc"])
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(9.5)
        r_desc.font.color.rgb = charcoal

        # Screenshot (showing code and output side-by-side)
        img_path = os.path.join(SHOTS_DIR, task["img"])
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.paragraph_format.space_before = Pt(2)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(6.8))

            # Caption
            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.space_before = Pt(1)
            p_cap.paragraph_format.space_after = Pt(4)
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(task["caption"])
            r_cap.font.name = "Calibri"
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(90, 90, 90)

        if idx < len(tasks) - 1:
            doc.add_page_break()

    doc.save(DOCX_OUT)
    doc.save(DOCX_LOCAL)
    print("Cleanly rebuilt DOCX:", DOCX_OUT)


if __name__ == "__main__":
    rebuild()
