"""Convierte INFORME.md a un PDF legible. Uso: python generar_pdf.py"""
from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, Flowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Informe_personas_San_Pedro_Mixtepec_2025.pdf"
NAVY = colors.HexColor("#173352")
TEAL = colors.HexColor("#137F82")
SOFT = colors.HexColor("#EAF5F4")
GOLD = colors.HexColor("#E4A946")
INK = colors.HexColor("#253847")
MUTED = colors.HexColor("#587080")
FONT_PAIRS = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf",
     "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
]
normal_font, bold_font = next(((a,b) for a,b in FONT_PAIRS if Path(a).exists() and Path(b).exists()), (None,None))
if normal_font is None:
    raise FileNotFoundError("Instala DejaVu Sans o Arial para generar el PDF")
pdfmetrics.registerFont(TTFont("DejaVu", normal_font))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", bold_font))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCustom", fontName="DejaVu-Bold", fontSize=21,
                          leading=27, textColor=NAVY, spaceAfter=12))
styles.add(ParagraphStyle(name="SubtitleCustom", fontName="DejaVu", fontSize=9.5,
                          leading=14, textColor=MUTED, spaceAfter=19))
styles.add(ParagraphStyle(name="H1Custom", fontName="DejaVu-Bold", fontSize=14,
                          leading=19, textColor=NAVY, spaceBefore=18, spaceAfter=8,
                          keepWithNext=True))
styles.add(ParagraphStyle(name="H2Custom", fontName="DejaVu-Bold", fontSize=10.5,
                          leading=15, textColor=TEAL, spaceBefore=14,
                          spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyCustom", fontName="DejaVu", fontSize=9.1,
                          leading=14.7, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle(name="QuoteCustom", parent=styles["BodyCustom"],
                          backColor=SOFT, borderPadding=11, borderColor=TEAL,
                          borderWidth=0.8, spaceBefore=8, spaceAfter=18,
                          fontSize=10, leading=16))
styles.add(ParagraphStyle(name="Cell", fontName="DejaVu", fontSize=7.6,
                          leading=11, textColor=INK))
styles.add(ParagraphStyle(name="CellHead", parent=styles["Cell"],
                          fontName="DejaVu-Bold", textColor=colors.white))
styles.add(ParagraphStyle(name="ListCustom", parent=styles["BodyCustom"],
                          leftIndent=16, firstLineIndent=-11))


def inline(markdown: str) -> str:
    t = html.escape(markdown, quote=False)
    t = re.sub(r"\[([^]]+)\]\((https?://[^)]+)\)",
               lambda m: f'<link href="{m.group(2)}" color="#137F82">{m.group(1)}</link>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`([^`]+)`", r"<font color='#137F82'>\1</font>", t)
    return t.replace("  ", " ")


class AgeBars(Flowable):
    def __init__(self, width: float):
        Flowable.__init__(self)
        self.width = width
        self.height = 106

    def draw(self):
        c = self.canv
        data = [("0–14", 22.94), ("15–29", 24.86), ("30–44", 23.85),
                ("45–64", 20.81), ("65+", 7.55)]
        c.setFont("DejaVu-Bold", 8)
        c.setFillColor(NAVY)
        c.drawString(0, 99, "Distribución por edad · % de la población")
        for i, (label, value) in enumerate(data):
            y = 80 - i * 18
            c.setFont("DejaVu", 8)
            c.setFillColor(INK)
            c.drawString(0, y + 2, label)
            c.setFillColor(SOFT)
            c.roundRect(68, y, self.width - 125, 10, 4, stroke=0, fill=1)
            c.setFillColor(TEAL if i < 4 else GOLD)
            c.roundRect(68, y, (self.width - 125) * value / 27, 10, 4, stroke=0, fill=1)
            c.setFillColor(NAVY)
            c.drawRightString(self.width, y + 2, f"{value:.2f} %".replace(".", ","))


def make_table(lines: list[str], width: float):
    matrix = [[s.strip() for s in line.strip().strip("|").split("|")] for line in lines]
    if len(matrix) > 1 and re.fullmatch(r"[\s:|\-]+", lines[1]):
        del matrix[1]
    n = len(matrix[0])
    if n == 3 and "Intervalo oficial" in matrix[0][-1]:
        widths = [width * .45, width * .19, width * .36]
    elif n == 3:
        widths = [width * .58, width * .22, width * .20]
    elif n == 4:
        widths = [width * .42, width * .19, width * .13, width * .26]
    else:
        widths = [width / n] * n
    cells = [[Paragraph(inline(value), styles["CellHead"] if row == 0 else styles["Cell"])
              for value in values] for row, values in enumerate(matrix)]
    table = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F8F9")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, -1), (-1, -1), .45, colors.HexColor("#D9E5E7")),
    ]))
    return table


def header_footer(canvas, doc):
    w, h = A4
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(.8)
    canvas.line(20 * mm, h - 18 * mm, w - 20 * mm, h - 18 * mm)
    canvas.setFont("DejaVu-Bold", 7)
    canvas.setFillColor(TEAL)
    canvas.drawString(20 * mm, h - 15 * mm, "EIC 2025  /  SAN PEDRO MIXTEPEC, DISTRITO 22")
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 14 * mm, "Fuente: INEGI · Análisis municipal de personas")
    canvas.drawRightString(w - 20 * mm, 14 * mm, str(doc.page))
    canvas.restoreState()


def main():
    w, h = A4
    margin = 20 * mm
    doc = BaseDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=margin,
                          rightMargin=margin, topMargin=25 * mm,
                          bottomMargin=22 * mm, title="Personas de San Pedro Mixtepec · EIC 2025",
                          author="Análisis con microdatos del INEGI")
    doc.addPageTemplates(PageTemplate(id="all", frames=[Frame(margin, 22 * mm,
        w - 2 * margin, h - 47 * mm, leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0)], onPage=header_footer))
    body_width = w - 2 * margin
    text = (ROOT / "INFORME.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    story = []
    i = 0
    saw_age = False
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("| "):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i]); i += 1
            story.extend([make_table(table_lines, body_width), Spacer(1, 8)])
            if not saw_age:
                story.extend([Spacer(1, 5), AgeBars(body_width), Spacer(1, 6)])
                saw_age = True
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["TitleCustom"]))
        elif line.startswith("**Encuesta Intercensal"):
            story.append(Paragraph(inline(line), styles["SubtitleCustom"]))
        elif line.startswith("**Corte"):
            story.append(Paragraph(inline(line), styles["SubtitleCustom"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["H1Custom"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["H2Custom"]))
        elif line.startswith("> "):
            story.append(Paragraph(inline(line[2:]), styles["QuoteCustom"]))
        elif re.match(r"(?:- |\d+\. )", line):
            content = re.sub(r"^(?:- |\d+\. )", "", line)
            story.append(Paragraph("•  " + inline(content), styles["ListCustom"]))
        else:
            paragraph = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"(?:#|\||>|- |\d+\. )", lines[i + 1].strip()):
                i += 1
                paragraph.append(lines[i].strip())
            story.append(Paragraph(inline(" ".join(paragraph)), styles["BodyCustom"]))
        i += 1
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    main()
