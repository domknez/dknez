#!/usr/bin/env python3
"""Regenerate assets/og.png (1200x630 social preview card).

Needs Pillow and the source portrait:
    python3 -m venv .venv && .venv/bin/pip install pillow
    .venv/bin/python tools/make-og.py path/to/portrait.png
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/portrait.jpg")
OUT = Path(__file__).resolve().parent.parent / "assets" / "og.png"

W, H = 1200, 630
BG = (36, 39, 58); CARD = (43, 46, 66); EDGE = (60, 64, 85)
FG = (202, 211, 245); FG2 = (165, 173, 203); FG3 = (128, 135, 162)
ACC = (166, 218, 149)

F = "/System/Library/Fonts/Supplemental/"
disp = ImageFont.truetype(F + "Arial Bold.ttf", 66)
disp_s = ImageFont.truetype(F + "Arial Bold.ttf", 30)
body = ImageFont.truetype(F + "Arial.ttf", 25)
mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 19)

img = Image.new("RGB", (W, H), BG)
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
gd.ellipse([-360, -400, 500, 460], fill=(58, 74, 74))
gd.ellipse([700, 380, 1400, 1080], fill=(45, 50, 78))
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(150)), 0.85)

PW, PH = 372, 466
PX, PY = W - PW - 64, (H - PH) // 2
shot = Image.open(SRC).convert("RGB")
s = max(PW / shot.width, PH / shot.height)
shot = shot.resize((round(shot.width * s), round(shot.height * s)), Image.LANCZOS)
oy = int((shot.height - PH) * 0.14)
shot = shot.crop(((shot.width - PW) // 2, oy, (shot.width - PW) // 2 + PW, oy + PH))
mask = Image.new("L", (PW, PH), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, PW - 1, PH - 1], 26, fill=255)
img.paste(shot, (PX, PY), mask)

d = ImageDraw.Draw(img, "RGBA")
d.rounded_rectangle([PX, PY, PX + PW - 1, PY + PH - 1], 26, outline=EDGE, width=2)
x, y = 72, 150
d.rounded_rectangle([x, y - 74, x + 214, y - 30], 22, fill=CARD, outline=EDGE, width=1)
d.ellipse([x + 18, y - 58, x + 30, y - 46], fill=ACC)
d.text((x + 40, y - 61), "ZAGREB, HR", font=mono, fill=FG2)
d.text((x, y - 4), "Domagoj Knez", font=disp, fill=FG)
d.text((x, y + 84), "Full-stack software engineer", font=disp_s, fill=ACC)
d.line([x, y + 146, x + 66, y + 146], fill=ACC, width=3)
ly = y + 176
for ln in ["Thirteen years across telecom, e-commerce,",
           "payments, insurance, SaaS and industrial AI."]:
    d.text((x, ly), ln, font=body, fill=FG2); ly += 36
cx, cy = x, ly + 26
for c in ["Python", "Django", "TypeScript", "React", "AWS"]:
    tw = d.textlength(c, font=mono)
    d.rounded_rectangle([cx, cy, cx + tw + 26, cy + 34], 17, fill=CARD, outline=EDGE, width=1)
    d.text((cx + 13, cy + 8), c, font=mono, fill=FG2)
    cx += tw + 35
d.text((x, H - 62), "knez.dev", font=mono, fill=FG3)

img.save(OUT, optimize=True)
print("wrote", OUT)
