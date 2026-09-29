from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR


BG = RGBColor(9, 12, 18)
CARD = RGBColor(17, 22, 31)
CARD_ALT = RGBColor(22, 29, 40)
BORDER = RGBColor(38, 45, 57)
TEXT = RGBColor(240, 243, 248)
MUTED = RGBColor(163, 171, 184)
ACCENT = RGBColor(102, 241, 190)

FONT_NAME = "Arial"


def _add_text(
    slide,
    text,
    x,
    y,
    w,
    h,
    size,
    color=TEXT,
    bold=False,
    align=PP_ALIGN.LEFT,
):
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )

    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.03)
    tf.margin_right = Inches(0.03)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)

    p = tf.paragraphs[0]
    p.text = str(text)
    p.alignment = align

    for run in p.runs:
        run.font.name = FONT_NAME
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color

    return box


def _background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG


def _card(slide, x, y, w, h, fill_color=CARD):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = BORDER
    return shape


def _footer(slide, index):
    _add_text(
        slide,
        f"{index:02d}",
        12.2,
        7.05,
        0.55,
        0.2,
        8,
        MUTED,
    )


def _flow_node(slide, text, x, y, w=1.75, h=0.75):
    shape = _card(slide, x, y, w, h, CARD_ALT)

    tf = shape.text_frame
    tf.clear()
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER

    for run in p.runs:
        run.font.name = FONT_NAME
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = TEXT

    return shape


def _arrow(slide, x1, y1, x2, y2):
    line = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(x1),
        Inches(y1),
        Inches(x2),
        Inches(y2),
    )
    line.line.color.rgb = ACCENT
    line.line.width = Pt(2)

    try:
        line.line.end_arrowhead = True
    except Exception:
        pass

    return line


def _bullet_card(slide, bullets):
    _card(slide, 0.75, 2.85, 6.35, 3.55)

    y = 3.18

    for bullet in bullets[:5]:
        _add_text(
            slide,
            "•",
            1.05,
            y,
            0.25,
            0.3,
            15,
            ACCENT,
            True,
        )

        _add_text(
            slide,
            bullet,
            1.38,
            y - 0.01,
            5.25,
            0.48,
            12,
            TEXT,
        )

        y += 0.58


def _pipeline_visual(slide, labels):
    _card(slide, 7.4, 2.85, 5.15, 3.55)

    _add_text(
        slide,
        "İŞ AKIŞI",
        7.75,
        3.15,
        2.0,
        0.25,
        8,
        ACCENT,
        True,
    )

    labels = labels[:4]

    if not labels:
        labels = ["GİRDİ", "SKILL'LER", "QA", "PPTX"]

    count = len(labels)
    node_w = 1.0 if count >= 4 else 1.25
    gap = 0.18
    total = count * node_w + (count - 1) * gap
    start_x = 7.4 + (5.15 - total) / 2
    y = 4.35

    nodes = []

    for i, label in enumerate(labels):
        x = start_x + i * (node_w + gap)
        node = _flow_node(slide, label, x, y, node_w, 0.8)
        nodes.append((x, node_w))

    for i in range(len(nodes) - 1):
        x, w = nodes[i]
        next_x, _ = nodes[i + 1]
        _arrow(
            slide,
            x + w,
            y + 0.4,
            next_x,
            y + 0.4,
        )


def _skill_visual(slide):
    _card(slide, 7.4, 2.85, 5.15, 3.55)

    _add_text(
        slide,
        "MODÜLER SKILL KATMANI",
        7.75,
        3.15,
        3.0,
        0.25,
        8,
        ACCENT,
        True,
    )

    items = [
        ("ARAŞTIRMA", 7.8, 3.75),
        ("SUNUM", 10.0, 3.75),
        ("DOKÜMAN", 7.8, 4.85),
        ("QA", 10.0, 4.85),
    ]

    for text, x, y in items:
        _flow_node(slide, text, x, y, 1.8, 0.75)

    _add_text(
        slide,
        "ORKESTRASYON",
        8.65,
        5.85,
        2.7,
        0.3,
        9,
        ACCENT,
        True,
        PP_ALIGN.CENTER,
    )


def _json_visual(slide):
    _card(slide, 7.4, 2.85, 5.15, 3.55)

    _add_text(
        slide,
        "YAPILANDIRILMIŞ JSON",
        7.75,
        3.15,
        2.5,
        0.25,
        8,
        ACCENT,
        True,
    )

    code = (
        '{\n'
        '  "title": "...",\n'
        '  "slides": [\n'
        '    {\n'
        '      "title": "...",\n'
        '      "content": [...]\n'
        '    }\n'
        '  ]\n'
        '}'
    )

    _add_text(
        slide,
        code,
        7.85,
        3.65,
        4.15,
        2.25,
        12,
        TEXT,
    )


def _demo_visual(slide):
    _card(slide, 7.4, 2.85, 5.15, 3.55)

    _add_text(
        slide,
        "DETERMİNİSTİK DEMO",
        7.75,
        3.15,
        2.8,
        0.25,
        8,
        ACCENT,
        True,
    )

    _flow_node(slide, "python app.py\n--demo", 7.85, 4.15, 1.8, 0.9)
    _flow_node(slide, "JSON\nDOĞRULAMA", 10.15, 4.15, 1.55, 0.9)

    _arrow(slide, 9.65, 4.6, 10.15, 4.6)

    _add_text(
        slide,
        "↓",
        10.65,
        5.2,
        0.5,
        0.35,
        18,
        ACCENT,
        True,
        PP_ALIGN.CENTER,
    )

    _add_text(
        slide,
        "DÜZENLENEBİLİR .PPTX",
        9.35,
        5.65,
        3.0,
        0.3,
        11,
        TEXT,
        True,
        PP_ALIGN.CENTER,
    )


def _adapter_visual(slide):
    _card(slide, 7.4, 2.85, 5.15, 3.55)

    _add_text(
        slide,
        "PLANLANAN GİRDİ ADAPTÖRLERİ",
        7.75,
        3.15,
        3.1,
        0.25,
        8,
        ACCENT,
        True,
    )

    _flow_node(slide, "PDF", 7.8, 3.75, 1.1, 0.7)
    _flow_node(slide, "DOCX", 7.8, 4.65, 1.1, 0.7)
    _flow_node(slide, "URL", 7.8, 5.55, 1.1, 0.7)

    _flow_node(
        slide,
        "NORMALİZE EDİLMİŞ\nKANIT",
        10.35,
        4.55,
        1.75,
        0.9,
    )

    _arrow(slide, 8.9, 4.1, 10.35, 4.8)
    _arrow(slide, 8.9, 5.0, 10.35, 5.0)
    _arrow(slide, 8.9, 5.9, 10.35, 5.2)


def _select_visual(slide, index, visual_text):
    visual_lower = str(visual_text).lower()

    if index == 2 or "skill" in visual_lower:
        _skill_visual(slide)

    elif index == 3 or "json" in visual_lower:
        _json_visual(slide)

    elif index == 4 or "terminal" in visual_lower:
        _demo_visual(slide)

    elif index == 6 or "adapter" in visual_lower:
        _adapter_visual(slide)

    elif index == 5 or "ollama" in visual_lower:
        _pipeline_visual(
            slide,
            ["OLLAMA", "JSON", "DOĞRULAYICI", "PPTX"],
        )

    else:
        _pipeline_visual(
            slide,
            ["GİRDİ", "SKILL'LER", "QA", "PPTX"],
        )


def export_pptx(data, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Kapak
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _background(slide)

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.65),
        Inches(0.75),
        Inches(0.08),
        Inches(5.8),
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()

    _add_text(
        slide,
        data.get("title", "Sunum"),
        1.05,
        1.55,
        10.8,
        1.6,
        30,
        TEXT,
        True,
    )

    _add_text(
        slide,
        data.get("subtitle", ""),
        1.08,
        3.25,
        9.8,
        0.8,
        18,
        MUTED,
    )

    _add_text(
        slide,
        "YAPAY ZEKA DESTEKLİ SUNUM OTOMASYONU",
        1.08,
        5.85,
        6.5,
        0.35,
        9,
        ACCENT,
        True,
    )

    # İçerik slaytları
    for i, s in enumerate(data.get("slides", []), start=1):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        _background(slide)

        _add_text(
            slide,
            f"SLAYT {i:02d}",
            0.75,
            0.55,
            2.0,
            0.3,
            8,
            ACCENT,
            True,
        )

        _add_text(
            slide,
            s.get("title", ""),
            0.75,
            1.0,
            11.6,
            0.7,
            25,
            TEXT,
            True,
        )

        _add_text(
            slide,
            s.get("key_message", ""),
            0.78,
            1.95,
            11.5,
            0.75,
            13,
            MUTED,
        )

        _bullet_card(slide, s.get("content", []))
        _select_visual(slide, i, s.get("visual", ""))

        _footer(slide, i)

        notes = s.get("speaker_notes")
        if notes:
            try:
                notes_slide = slide.notes_slide
                notes_slide.notes_text_frame.text = str(notes)
            except Exception:
                pass

    prs.save(output_path)
    return output_path


