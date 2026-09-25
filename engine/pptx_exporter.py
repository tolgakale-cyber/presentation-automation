from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE


BG = RGBColor(9, 12, 18)
CARD = RGBColor(17, 22, 31)
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
    auto_fit=False,
):
    box = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h),
    )

    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True

    if auto_fit:
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE

    p = tf.paragraphs[0]
    p.text = str(text)
    p.font.name = FONT_NAME
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color

    return box


def _background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG


def _footer(slide, index):
    _add_text(
        slide,
        f"{index:02d}",
        12.2,
        7.05,
        0.6,
        0.25,
        8,
        MUTED,
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
        False,
        True,
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
            False,
            True,
        )

        # İçerik kartı
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.75),
            Inches(2.85),
            Inches(7.65),
            Inches(3.55),
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD
        shape.line.color.rgb = RGBColor(38, 45, 57)

        y = 3.18

        for bullet in s.get("content", [])[:5]:
            _add_text(
                slide,
                "•",
                1.08,
                y,
                0.3,
                0.35,
                14,
                ACCENT,
                True,
            )

            _add_text(
                slide,
                bullet,
                1.42,
                y - 0.02,
                6.45,
                0.48,
                13,
                TEXT,
                False,
                True,
            )

            y += 0.58

        # Görsel yönlendirme kartı
        visual_card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(8.7),
            Inches(2.85),
            Inches(3.85),
            Inches(3.55),
        )
        visual_card.fill.solid()
        visual_card.fill.fore_color.rgb = CARD
        visual_card.line.color.rgb = RGBColor(38, 45, 57)

        _add_text(
            slide,
            "GÖRSEL YÖNLENDİRME",
            9.05,
            3.18,
            2.9,
            0.3,
            8,
            ACCENT,
            True,
        )

        _add_text(
            slide,
            s.get("visual", ""),
            9.05,
            3.7,
            2.95,
            1.65,
            13,
            TEXT,
            False,
            True,
        )

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