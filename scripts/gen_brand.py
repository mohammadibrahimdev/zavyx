"""Generate the Zavyx brand artwork used by this README.

Requires Pillow (`pip install pillow`) and Windows fonts (Segoe UI). Run from the
repo root:

    python scripts/gen_brand.py

Outputs (in assets/):
    zavyx-mark.svg / zavyx-mark-512.png   round brand mark (avatar, favicon)
    banner.svg / banner.png               README header (1280x400)
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
FONT_BLACK = r"C:\Windows\Fonts\seguibl.ttf"   # Segoe UI Black
FONT_SEMI = r"C:\Windows\Fonts\seguisb.ttf"    # Segoe UI Semibold

# Brand gradient: Zavyx violet into pink.
VIOLET = (124, 92, 255)
PINK = (255, 92, 168)
BG_TOP = (15, 12, 29)
BG_BOTTOM = (36, 26, 77)

# "Z" mark on a 256-unit canvas, centred in the circle.
Z = [(74, 70), (182, 70), (182, 100), (112, 156), (182, 156),
     (182, 186), (74, 186), (74, 156), (144, 100), (74, 100)]

TAGLINE = "Free & open-source tools for everyone"
BYLINE = "by Mohammad Ibrahim  ·  github.com/mohammadibrahimdev"


def diagonal_gradient(size, a, b):
    """Square image with a top-left to bottom-right gradient from colour a to b."""
    small = Image.new("RGB", (64, 64))
    px = small.load()
    for y in range(64):
        for x in range(64):
            t = (x + y) / 126
            px[x, y] = tuple(round(c1 + (c2 - c1) * t) for c1, c2 in zip(a, b))
    return small.resize((size, size), Image.BICUBIC)


def mark(size):
    s = size * 4
    k = s / 256
    grad = diagonal_gradient(s, VIOLET, PINK).convert("RGBA")
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, s - 1, s - 1], fill=255)
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mask)
    ImageDraw.Draw(img).polygon([(x * k, y * k) for x, y in Z], fill=(255, 255, 255, 255))
    return img.resize((size, size), Image.LANCZOS)


def banner(width=1280, height=400):
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / (height - 1)
        draw.line([(0, y), (width, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM)))
    # Soft glow behind the mark.
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([60, 40, 440, 360], fill=VIOLET + (110,))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(70)))

    m = mark(220)
    img.paste(m, (140, 90), m)

    draw = ImageDraw.Draw(img)
    title = ImageFont.truetype(FONT_BLACK, 132)
    x = 410
    for ch in "ZAVYX":  # manual letter spacing
        draw.text((x, 78), ch, font=title, fill=(255, 255, 255))
        x += draw.textlength(ch, font=title) + 14
    draw.text((414, 238), TAGLINE, font=ImageFont.truetype(FONT_SEMI, 36), fill=(214, 206, 255))
    draw.text((416, 296), BYLINE, font=ImageFont.truetype(FONT_SEMI, 24), fill=(150, 141, 200))
    return img.convert("RGB")


MARK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#{violet}"/>
      <stop offset="1" stop-color="#{pink}"/>
    </linearGradient>
  </defs>
  <circle cx="128" cy="128" r="128" fill="url(#g)"/>
  <polygon fill="#fff" points="{points}"/>
</svg>
"""

BANNER_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 400" width="1280" height="400">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#{bg_top}"/>
      <stop offset="1" stop-color="#{bg_bottom}"/>
    </linearGradient>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#{violet}"/>
      <stop offset="1" stop-color="#{pink}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#{violet}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#{violet}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1280" height="400" fill="url(#bg)"/>
  <circle cx="250" cy="200" r="230" fill="url(#glow)"/>
  <g transform="translate(140 90) scale(0.859375)">
    <circle cx="128" cy="128" r="128" fill="url(#g)"/>
    <polygon fill="#fff" points="{points}"/>
  </g>
  <text x="410" y="200" fill="#fff" font-family="'Segoe UI Black','Arial Black',sans-serif" font-weight="900" font-size="132" letter-spacing="14">ZAVYX</text>
  <text x="414" y="275" fill="#d6ceff" font-family="'Segoe UI',Arial,sans-serif" font-weight="600" font-size="36">{tagline}</text>
  <text x="416" y="322" fill="#968dc8" font-family="'Segoe UI',Arial,sans-serif" font-weight="600" font-size="24">{byline}</text>
</svg>
"""


def hexc(rgb):
    return "%02x%02x%02x" % rgb


def main():
    os.makedirs(ASSETS, exist_ok=True)
    points = " ".join(f"{x},{y}" for x, y in Z)
    with open(os.path.join(ASSETS, "zavyx-mark.svg"), "w", encoding="utf-8") as f:
        f.write(MARK_SVG.format(violet=hexc(VIOLET), pink=hexc(PINK), points=points))
    with open(os.path.join(ASSETS, "banner.svg"), "w", encoding="utf-8") as f:
        f.write(BANNER_SVG.format(
            bg_top=hexc(BG_TOP), bg_bottom=hexc(BG_BOTTOM), violet=hexc(VIOLET), pink=hexc(PINK),
            points=points, tagline=TAGLINE, byline=BYLINE.replace("·", "&#183;"),
        ))
    mark(512).save(os.path.join(ASSETS, "zavyx-mark-512.png"))
    banner().save(os.path.join(ASSETS, "banner.png"))
    print("brand assets written")


if __name__ == "__main__":
    main()
