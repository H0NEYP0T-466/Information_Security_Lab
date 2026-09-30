#!/usr/bin/env python3
import os
import sys
import shutil
from PIL import Image as PILImage

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Preformatted, Image as RLImage
)

# === COLORS ===
G  = HexColor("#1B5E20")   # Primary green
LG = HexColor("#E8F5E9")   # Light green
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
SB_W = 12 * mm           # Sidebar width

# === STYLES ===
def S(name, font="Times-Roman", size=12, color=TD, align=TA_LEFT,
      bold=False, italic=False, sa=4, sb=0, li=0, leading=None):
    return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color,
        alignment=align, spaceAfter=sa, spaceBefore=sb,
        leading=leading or (size * 1.3), leftIndent=li)

s_ct   = S("ct",   size=10, color=G,  align=TA_CENTER, bold=True, sa=3)
s_ctt  = S("ctt",  size=18, color=G,  align=TA_CENTER, bold=True, sa=4)
s_cs   = S("cs",   size=11, color=SG, align=TA_CENTER, italic=True, sa=6)
s_cl   = S("cl",   size=10, color=G,  bold=True)
s_cv   = S("cv",   size=10, color=TD)

s_h1   = S("h1",   size=13, color=G,  bold=True, sa=4, sb=2)
s_h2   = S("h2",   size=10, color=AG, bold=True, sa=3, sb=6)
s_body = S("body", size=10, color=TD, sa=3, leading=14)
s_q    = S("q",    size=9.5, color=TD, sa=0, leading=13.5)

code_style = ParagraphStyle(
    "CodeStyle",
    fontName="Courier",
    fontSize=8.5,
    leading=11.5,
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
    canvas.setFont("Times-Roman", 9)
    canvas.setFillColor(FG)
    canvas.drawString(LM, PAGE_H - 0.6 * inch, "Information Security Lab  |  Lab Manual 02")
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

    main_items.append(Spacer(1, 3 * mm))
    main_items.append(Paragraph("LAHORE GARRISON UNIVERSITY", S("lgu_u", size=13, color=G, align=TA_CENTER, bold=True, sa=2)))
    main_items.append(Paragraph("Department of Computer Science", S("lgu_d", size=10, color=SG, align=TA_CENTER, sa=4)))
    main_items.append(Spacer(1, 2 * mm))
    main_items.append(Paragraph("INFORMATION SECURITY LAB", s_ct))
    main_items.append(Paragraph("LAB MANUAL # 2", s_ctt))
    main_items.append(Paragraph("Data Structures in Python - Lists, Tuples, Sets & Dictionaries", s_cs))
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
        [Paragraph("<b>CONTEXT:</b>", s_cl), Paragraph("Lab Manual # 2 - Practical Tasks", s_cv)],
    ]
    it = Table(info, colWidths=[38 * mm, main_w - 38 * mm])
    it.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, HexColor("#EEEEEE")),
    ]))
    main_items.append(it)
    main_items.append(Spacer(1, 5 * mm))
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

# === QUESTION BUILDER ===
def build_task_page(task_num, task_title, question_text, code_text, img_path, max_img_h):
    items = []
    
    # Task Header
    items.append(Paragraph(f"<b>Task {task_num}: {task_title}</b>", s_h1))
    items.append(HRFlowable(width="100%", thickness=0.8, color=AG, spaceAfter=4))
    
    # Question Callout Box
    q_content = [
        [Paragraph(f"<b>Question #{task_num}:</b> {question_text}", s_q)]
    ]
    q_tbl = Table(q_content, colWidths=[CW])
    q_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LG),
        ('LINELEFT', (0,0), (0,-1), 2.5, AG),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor("#C8E6C9")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    items.append(q_tbl)
    items.append(Spacer(1, 3 * mm))
    
    # Source Code Section
    items.append(Paragraph("<b>Source Code:</b>", s_h2))
    pre = Preformatted(code_text.strip(), code_style)
    code_tbl = Table([[pre]], colWidths=[CW])
    code_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CODE),
        ('LINELEFT', (0,0), (0,-1), 2.5, G),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_CODE),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    items.append(code_tbl)
    items.append(Spacer(1, 3 * mm))
    
    # Execution Output Screenshot
    items.append(Paragraph("<b>Execution Output:</b>", s_h2))
    img_element = styled_img(img_path, max_w=CW - 10, max_h=max_img_h)
    items.append(img_element)
    
    return items

def main():
    code_dir = "/home/honeypot/Univeristy_Data/IF(L)/LAB(2)/Code"
    output_pdf = "/home/honeypot/Univeristy_Data/IF(L)/LAB(2)/Information_Security_Lab_Manual_02.pdf"
    desktop_pdf = "/home/honeypot/Desktop/Information_Security_Lab_Manual_02.pdf"

    # Read Python files
    with open(f"{code_dir}/MergeSort.py") as f:
        code_t1 = f.read()
    with open(f"{code_dir}/SmallLarge.py") as f:
        code_t2 = f.read()
    with open(f"{code_dir}/birthday.py") as f:
        code_t3 = f.read()
    with open(f"{code_dir}/extractkeys.py") as f:
        code_t4 = f.read()

    tasks = [
        {
            "num": 1,
            "title": "Merge & Sort Two Lists",
            "q": "Create two lists from user input, merge them together, and display the resulting combined list in sorted order.",
            "code": code_t1,
            "img": f"{code_dir}/MergeSort.png",
            "max_img_h": 220,
        },
        {
            "num": 2,
            "title": "Smallest & Largest Element",
            "q": "Reusing the merged list concept from user input, determine and display the smallest and largest integer values from the collection.",
            "code": code_t2,
            "img": f"{code_dir}/SmallLarge.png",
            "max_img_h": 210,
        },
        {
            "num": 3,
            "title": "Birthday Dictionary Lookup",
            "q": "Build a dictionary mapping names to birthdays, prompt the user for a name, and print the corresponding birthday or an absence notice.",
            "code": code_t3,
            "img": f"{code_dir}/Birthday.png",
            "max_img_h": 190,
        },
        {
            "num": 4,
            "title": "Extract Selected Keys",
            "q": "Given a sample dictionary containing multiple fields and a list of specific keys, extract only those designated key-value pairs into a new dictionary.",
            "code": code_t4,
            "img": f"{code_dir}/extractkeys.png",
            "max_img_h": 195,
        },
    ]

    elements = build_cover()

    for idx, t in enumerate(tasks):
        page_items = build_task_page(
            task_num=t["num"],
            task_title=t["title"],
            question_text=t["q"],
            code_text=t["code"],
            img_path=t["img"],
            max_img_h=t["max_img_h"]
        )
        elements.extend(page_items)
        if idx < len(tasks) - 1:
            elements.append(PageBreak())

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
    print(f"Copied to: {desktop_pdf}")

if __name__ == "__main__":
    main()
