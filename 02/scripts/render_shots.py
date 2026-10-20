#!/usr/bin/env python3
"""Перетворює текстові логи сеансів sqlite3 на зображення вікна консолі."""
import os
import glob
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(BASE, "logs")
SHOTS = os.path.join(BASE, "screenshots")

FONT_PATH = "/System/Library/Fonts/Menlo.ttc"
FONT_SIZE = 26          # рендеримо збільшено, щоб у документі було чітко
PAD = 18
BG = (252, 252, 252)
FG = (24, 24, 24)
BORDER = (150, 150, 150)
SCALE = 2               # для чіткості на друці


def render(text, out_path):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE * SCALE)
    lines = text.rstrip("\n").split("\n")
    probe = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(probe)
    char_w = d.textlength("M", font=font)
    line_h = int(FONT_SIZE * SCALE * 1.4)
    width = int(max((len(l) for l in lines), default=20) * char_w) + 2 * PAD * SCALE
    height = line_h * len(lines) + 2 * PAD * SCALE
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width - 1, height - 1], outline=BORDER, width=SCALE)
    for i, line in enumerate(lines):
        d.text((PAD * SCALE, PAD * SCALE + i * line_h), line, font=font, fill=FG)
    img.save(out_path, "PNG", dpi=(200, 200))
    return img.size


def main():
    os.makedirs(SHOTS, exist_ok=True)
    n = 0
    for log in sorted(glob.glob(os.path.join(LOGS, "*.txt"))):
        name = os.path.splitext(os.path.basename(log))[0]
        with open(log) as f:
            text = f.read()
        size = render(text, os.path.join(SHOTS, name + ".png"))
        n += 1
        print("%-16s %dx%d" % (name, size[0], size[1]))
    print("\nСтворено %d зображень" % n)


if __name__ == "__main__":
    main()
