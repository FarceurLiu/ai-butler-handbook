#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
COVER_PREVIEW = ROOT / "assets" / "cover-preview.png"
COVER_PREVIEW_EN = ROOT / "assets" / "cover-preview-en.png"
SOCIAL_PREVIEW = ROOT / "assets" / "social-preview.png"
SOCIAL_PREVIEW_ZH = ROOT / "assets" / "social-preview-zh.png"
SOCIAL_PREVIEW_EN = ROOT / "assets" / "social-preview-en.png"

WIDTH = 1200
HEIGHT = 630

FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def draw_multiline(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    text_font: ImageFont.ImageFont,
    fill: str,
    line_gap: int,
) -> None:
    x, y = xy
    for line in text.splitlines():
        draw.text((x, y), line, font=text_font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=text_font)
        y += bbox[3] - bbox[1] + line_gap


def rounded_image(image: Image.Image, radius: int) -> Image.Image:
    image = image.convert("RGBA")
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, image.width, image.height), radius=radius, fill=255)
    image.putalpha(mask)
    return image


def draw_badge(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str) -> int:
    x, y = xy
    badge_font = font(24)
    padding_x = 18
    padding_y = 10
    bbox = draw.textbbox((0, 0), text, font=badge_font)
    width = bbox[2] - bbox[0] + padding_x * 2
    height = bbox[3] - bbox[1] + padding_y * 2
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=9,
        fill=(255, 255, 255, 245),
        outline="#b8cef8",
        width=2,
    )
    draw.text((x + padding_x, y + padding_y - 2), text, font=badge_font, fill="#172033")
    return width


def paste_cover(canvas: Image.Image, cover_path: Path) -> None:
    cover = Image.open(cover_path).convert("RGBA")
    cover.thumbnail((360, 510), Image.Resampling.LANCZOS)
    x = 741
    y = 60

    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (x + 10, y + 14, x + cover.width + 10, y + cover.height + 14),
        radius=14,
        fill=(24, 52, 93, 35),
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)))

    border = ImageDraw.Draw(canvas)
    border.rounded_rectangle(
        (x - 2, y - 2, x + cover.width + 2, y + cover.height + 2),
        radius=15,
        fill="#ffffff",
        outline="#b8cef8",
        width=2,
    )
    canvas.alpha_composite(rounded_image(cover, 12), (x, y))


def generate_social_preview(output: Path = SOCIAL_PREVIEW, locale: str = "zh") -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "#f7fbff")
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.ellipse((-260, -260, 640, 790), fill=(219, 232, 255, 215))
    draw.ellipse((650, 88, 1395, 730), fill=(224, 244, 247, 190))

    grid_color = (203, 220, 248, 95)
    for x in range(0, WIDTH + 1, 64):
        draw.line((x, 0, x, HEIGHT), fill=grid_color, width=1)
    for y in range(0, HEIGHT + 1, 64):
        draw.line((0, y, WIDTH, y), fill=grid_color, width=1)

    if locale == "en":
        eyebrow = "FREE PUBLIC HANDBOOK"
        title = "AI Work Assistant\nHandbook"
        subtitle = "Build repeatable AI workflows:\nassign clearly, verify output,\nrefine, and save what works."
        badges = ("22 chapters", "4 Skill cases", "English edition")
        cover_path = COVER_PREVIEW_EN
        title_size = 60
    else:
        eyebrow = "免費公開版手冊"
        title = "從零開始養成我的\nAI 管家"
        subtitle = "建立可重複使用的 AI 工作流：\n清楚交辦、驗收輸出、復盤優化，\n把有效做法留下來。"
        badges = ("22 章養成路線", "4 個 Skill 案例", "繁體中文")
        cover_path = COVER_PREVIEW
        title_size = 60

    draw.text((76, 86), eyebrow, font=font(28), fill="#2563eb")
    draw_multiline(draw, (76, 145), title, font(title_size), "#111827", line_gap=12)
    draw_multiline(draw, (78, 334), subtitle, font(29), "#53637a", line_gap=9)

    badge_y = 486
    x = 77
    for text in badges:
        width = draw_badge(draw, (x, badge_y), text)
        x += width + 14

    draw.text(
        (77, 574),
        "farceurliu.github.io/ai-butler-handbook",
        font=font(20),
        fill="#66758d",
    )

    paste_cover(canvas, cover_path)
    canvas.convert("RGB").save(output, "PNG", optimize=True)


def generate_social_previews() -> None:
    generate_social_preview(SOCIAL_PREVIEW_ZH, "zh")
    generate_social_preview(SOCIAL_PREVIEW_EN, "en")
    generate_social_preview(SOCIAL_PREVIEW, "zh")


if __name__ == "__main__":
    generate_social_previews()
