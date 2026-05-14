#!/usr/bin/env python3
"""Generate og-image.png for the resume site. Run from repo root: python3 scripts/gen_og.py"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = "og-image.png"

FONTS_BASE = "/usr/share/fonts/truetype/liberation"
FONT_BOLD   = os.path.join(FONTS_BASE, "LiberationSans-Bold.ttf")
FONT_REG    = os.path.join(FONTS_BASE, "LiberationSans-Regular.ttf")

BG          = (4, 7, 15)        # --bg dark
PANEL       = (10, 16, 31)      # card surface
ACCENT      = (47, 100, 255)    # --accent
ACCENT2     = (103, 232, 200)   # --accent2
FG          = (238, 244, 255)   # --fg dark
MUTED       = (169, 182, 216)   # --muted dark
TAG_BG      = (18, 28, 54)
TAG_BORDER  = (47, 100, 255, 60)

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

# --- background gradient strips (subtle depth) ---
for y in range(H):
    t = y / H
    r = int(BG[0] + (PANEL[0] - BG[0]) * t * 0.6)
    g = int(BG[1] + (PANEL[1] - BG[1]) * t * 0.6)
    b = int(BG[2] + (PANEL[2] - BG[2]) * t * 0.6)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- top accent bar ---
draw.rectangle([0, 0, W, 5], fill=ACCENT)

# --- subtle radial glow top-left ---
for r in range(320, 0, -4):
    alpha = int(18 * (1 - r / 320))
    draw.ellipse([-r + 160, -r + 180, r + 160, r + 180], fill=(*ACCENT, alpha))

# --- card panel ---
pad = 72
cx, cy = pad, 90
cw, ch = W - pad * 2, H - 160
draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=28,
                        fill=(*PANEL, 230), outline=(*ACCENT, 40), width=1)

# --- fonts ---
try:
    fn_name   = ImageFont.truetype(FONT_BOLD, 76)
    fn_title  = ImageFont.truetype(FONT_BOLD, 34)
    fn_strap  = ImageFont.truetype(FONT_REG,  28)
    fn_tag    = ImageFont.truetype(FONT_REG,  22)
    fn_url    = ImageFont.truetype(FONT_REG,  20)
except Exception as e:
    print(f"Font error: {e} — using default")
    fn_name = fn_title = fn_strap = fn_tag = fn_url = ImageFont.load_default()

# --- name ---
name = "Brandon S. Clark"
bbox = draw.textbbox((0, 0), name, font=fn_name)
nx = (W - (bbox[2] - bbox[0])) // 2
draw.text((nx, 148), name, font=fn_name, fill=FG)

# --- title ---
title = "Senior Software Engineer"
bbox = draw.textbbox((0, 0), title, font=fn_title)
tx = (W - (bbox[2] - bbox[0])) // 2
draw.text((tx, 252), title, font=fn_title, fill=ACCENT)

# --- strap ---
strap = "Cloud · Data · IoT Platforms"
bbox = draw.textbbox((0, 0), strap, font=fn_strap)
sx = (W - (bbox[2] - bbox[0])) // 2
draw.text((sx, 306), strap, font=fn_strap, fill=MUTED)

# --- divider ---
div_y = 362
draw.line([(cx + 60, div_y), (cx + cw - 60, div_y)], fill=(*ACCENT, 40), width=1)

# --- skill tags ---
skills = ["AWS", "IoT", "Terraform", "TypeScript", "Python", "Node.js", "Serverless"]
tag_h = 38
padding_x = 20
gap = 14
total_w = 0
widths = []
for s in skills:
    bb = draw.textbbox((0, 0), s, font=fn_tag)
    tw = bb[2] - bb[0] + padding_x * 2
    widths.append(tw)
    total_w += tw + gap
total_w -= gap

row_x = (W - total_w) // 2
row_y = 384
for i, s in enumerate(skills):
    tw = widths[i]
    draw.rounded_rectangle([row_x, row_y, row_x + tw, row_y + tag_h],
                            radius=8, fill=TAG_BG, outline=(*ACCENT, 55), width=1)
    bb = draw.textbbox((0, 0), s, font=fn_tag)
    th = bb[3] - bb[1]
    draw.text((row_x + padding_x, row_y + (tag_h - th) // 2 - 1), s,
              font=fn_tag, fill=ACCENT2)
    row_x += tw + gap

# --- url ---
url = "theghostarbiter.github.io/static-resume"
bbox = draw.textbbox((0, 0), url, font=fn_url)
ux = (W - (bbox[2] - bbox[0])) // 2
draw.text((ux, 456), url, font=fn_url, fill=(*MUTED, 160))

# --- bottom accent line ---
draw.rectangle([0, H - 4, W, H], fill=ACCENT)

img.save(OUT, "PNG", optimize=True)
print(f"Saved {OUT} ({W}x{H})")
