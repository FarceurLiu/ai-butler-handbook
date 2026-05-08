#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "downloads" / "ai-work-assistant-handbook_public-edition_v1.0_en.md"
OUTPUT = ROOT / "downloads" / "ai-work-assistant-handbook_public-edition_v1.0_en.pdf"
SITE_URL = "https://farceurliu.github.io/ai-butler-handbook/"
WATERMARK = "FREE PUBLIC EDITION | Farceur Liu | farceurliu.github.io/ai-butler-handbook/"


def register_fonts() -> str:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    return "STSong-Light"


CJK_FONT = register_fonts()
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName=FONT_BOLD,
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#101828"),
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=13,
            leading=19,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475467"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName=FONT_BOLD,
            fontSize=21,
            leading=27,
            textColor=colors.HexColor("#101828"),
            spaceBefore=18,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName=FONT_BOLD,
            fontSize=16,
            leading=22,
            textColor=colors.HexColor("#1d4ed8"),
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName=FONT_BOLD,
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#344054"),
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=10.2,
            leading=15.5,
            textColor=colors.HexColor("#101828"),
            spaceAfter=6,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=10.2,
            leading=15.5,
            leftIndent=12,
            borderColor=colors.HexColor("#d6dfeb"),
            borderWidth=0.8,
            borderPadding=6,
            backColor=colors.HexColor("#f3f7fc"),
            textColor=colors.HexColor("#344054"),
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.8,
            leading=10.4,
            leftIndent=6,
            rightIndent=6,
            backColor=colors.HexColor("#f8fafc"),
            borderColor=colors.HexColor("#d6dfeb"),
            borderWidth=0.5,
            borderPadding=6,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=10.2,
            leading=15.5,
            leftIndent=14,
            firstLineIndent=0,
            textColor=colors.HexColor("#101828"),
        ),
        "cell": ParagraphStyle(
            "Cell",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=8.2,
            leading=10.8,
            textColor=colors.HexColor("#101828"),
        ),
    }


STYLES = styles()


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" color="#1d4ed8">\1</a>', text)
    text = re.sub(
        r"([\u3000-\u303f\u3400-\u9fff\uff00-\uffef]+)",
        rf'<font name="{CJK_FONT}">\1</font>',
        text,
    )
    return text


def split_table_row(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def flush_table(story: list, table_lines: list[str]) -> None:
    if len(table_lines) < 2:
        table_lines.clear()
        return
    rows = [split_table_row(line) for line in table_lines]
    table_lines.clear()
    if not re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", rows_to_raw(rows[1])):
        return
    data = []
    for idx, row in enumerate(rows[:1] + rows[2:]):
        style = STYLES["cell"]
        data.append([Paragraph(inline(cell), style) for cell in row])
    if not data:
        return
    col_count = max(len(row) for row in data)
    for row in data:
        while len(row) < col_count:
            row.append(Paragraph("", STYLES["cell"]))
    table = Table(data, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf1ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#101828")),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#d6dfeb")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([table, Spacer(1, 8)])


def rows_to_raw(row: list[str]) -> str:
    return "|" + "|".join(row) + "|"


def flush_list(story: list, items: list[str], ordered: bool) -> None:
    if not items:
        return
    for idx, item in enumerate(items, start=1):
        bullet = f"{idx}." if ordered else "-"
        story.append(Paragraph(inline(item), STYLES["bullet"], bulletText=bullet))
    story.append(Spacer(1, 5))
    items.clear()


def markdown_to_story(markdown: str) -> list:
    story: list = []
    list_items: list[str] = []
    list_ordered = False
    table_lines: list[str] = []
    code_lines: list[str] = []
    in_code = False
    first_title = True

    for raw in markdown.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_lines), STYLES["code"], maxLineLength=92))
                story.append(Spacer(1, 8))
                code_lines = []
                in_code = False
            else:
                flush_list(story, list_items, list_ordered)
                flush_table(story, table_lines)
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue

        if not stripped:
            flush_list(story, list_items, list_ordered)
            flush_table(story, table_lines)
            continue

        if stripped == "---":
            flush_list(story, list_items, list_ordered)
            flush_table(story, table_lines)
            story.append(Spacer(1, 8))
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_list(story, list_items, list_ordered)
            table_lines.append(stripped)
            continue

        flush_table(story, table_lines)

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_list(story, list_items, list_ordered)
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1 and first_title:
                story.append(Paragraph(inline(text), STYLES["title"]))
                first_title = False
            elif level == 1:
                story.append(PageBreak())
                story.append(Paragraph(inline(text), STYLES["h1"]))
            elif level == 2:
                if re.match(r"^(\d+\.|Appendix )", text):
                    story.append(PageBreak())
                story.append(Paragraph(inline(text), STYLES["h1"]))
            elif level == 3:
                story.append(Paragraph(inline(text), STYLES["h2"]))
            else:
                story.append(Paragraph(inline(text), STYLES["h3"]))
            continue

        quote = re.match(r"^>\s*(.+)$", stripped)
        if quote:
            flush_list(story, list_items, list_ordered)
            story.append(Paragraph(inline(quote.group(1)), STYLES["quote"]))
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        number = re.match(r"^\d+\.\s+(.+)$", stripped)
        if bullet or number:
            ordered = bool(number)
            if list_items and ordered != list_ordered:
                flush_list(story, list_items, list_ordered)
            list_ordered = ordered
            list_items.append(bullet.group(1) if bullet else number.group(1))
            continue

        flush_list(story, list_items, list_ordered)
        story.append(Paragraph(inline(stripped), STYLES["body"]))

    if in_code:
        story.append(Preformatted("\n".join(code_lines), STYLES["code"], maxLineLength=92))
    flush_list(story, list_items, list_ordered)
    flush_table(story, table_lines)
    return story


def draw_page(canvas, doc) -> None:
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#2563eb"))
    canvas.setFillAlpha(0.055)
    canvas.setFont("Helvetica-Bold", 16)
    canvas.translate(width / 2, height / 2)
    canvas.rotate(35)
    for y in range(int(-height), int(height) + 150, 150):
        canvas.drawCentredString(0, y, WATERMARK)
    canvas.restoreState()

    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#98a2b3"))
    canvas.setFont("Helvetica", 7)
    canvas.drawString(18 * mm, 11 * mm, "AI Work Assistant Handbook - Free Public Edition")
    canvas.drawRightString(width - 18 * mm, 11 * mm, f"{doc.page}")
    canvas.restoreState()


def build_pdf() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    story = markdown_to_story(markdown)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title="AI Work Assistant Handbook",
        author="Farceur Liu",
        subject="Free public handbook for repeatable AI workflows",
    )
    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
