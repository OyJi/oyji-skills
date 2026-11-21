#!/usr/bin/env python3
"""Big thumbnail headline with a stroke, added locally so the letters are exact (Kazakh letters
and Russian included). Image models bend letters, so a headline is never taken from the model.

    python3 -I thumb_text.py spec.json

spec.json:
{
  "image": "pick.png",
  "out": "thumb.png",
  "text": "БҰЛ НЕ БОЛДЫ?",            # 2 to 4 words; use \\n for a manual line break
  "preset": "beast",                 # beast | fire | lime | clean
  "position": "left",                # left | right | top | bottom | center
  "size": 0.16                       # text height as a fraction of the image height (0.08 - 0.30)
}
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

NEED = "ӘәІіҢңҒғҮүҰұҚқӨөҺһ"
FONTS = [("/System/Library/Fonts/Helvetica.ttc", 1), ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0),
         ("C:/Windows/Fonts/arialbd.ttf", 0)]
PRESETS = {  # fill, stroke, stroke width (fraction of font size), shadow
    "beast": {"fill": [(255, 232, 40), (255, 190, 0)], "stroke": (0, 0, 0), "sw": 0.11, "shadow": 0.5},
    "fire": {"fill": [(255, 225, 90), (255, 80, 20)], "stroke": (60, 8, 0), "sw": 0.09, "shadow": 0.5},
    "lime": {"fill": [(200, 255, 60), (120, 255, 30)], "stroke": (10, 40, 0), "sw": 0.10, "shadow": 0.45},
    "clean": {"fill": [(255, 255, 255), (235, 235, 235)], "stroke": (0, 0, 0, 0), "sw": 0.0, "shadow": 0.7},
}


def pick_font(size):
    for path, idx in FONTS:
        if not os.path.exists(path):
            continue
        try:
            from fontTools.ttLib import TTFont, TTCollection
            f = TTCollection(path).fonts[idx] if path.endswith(".ttc") else TTFont(path)
            if not all(ord(c) in f.getBestCmap() for c in NEED):
                continue
        except Exception:
            pass
        return ImageFont.truetype(path, size, index=idx)
    sys.exit("No bold font with Kazakh letters found; install DejaVu Sans Bold or Noto Sans Bold.")


def fit_lines(draw, text, size, max_w):
    lines = []
    for part in text.split("\n"):
        words, cur = part.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=pick_font(size)) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def main(spec):
    im = Image.open(spec["image"]).convert("RGBA")
    W, H = im.size
    P = PRESETS[spec.get("preset", "beast")]
    size = int(H * float(spec.get("size", 0.16)))
    margin = int(W * 0.04)
    d = ImageDraw.Draw(im)
    pos = spec.get("position", "left")
    max_w = int(W * (0.55 if pos in ("left", "right") else 0.9))

    # shrink until the longest word fits the box
    while True:
        lines = fit_lines(d, spec["text"].upper(), size, max_w)
        font = pick_font(size)
        widest = max(d.textlength(l, font=font) for l in lines)
        if widest <= max_w or size < 24:
            break
        size = int(size * 0.92)
    lh = int(size * 1.08)
    block_h = lh * len(lines)
    block_w = int(widest)

    if pos == "left":
        x0, y0 = margin, (H - block_h) // 2
    elif pos == "right":
        x0, y0 = W - margin - block_w, (H - block_h) // 2
    elif pos == "top":
        x0, y0 = (W - block_w) // 2, margin
    elif pos == "bottom":
        x0, y0 = (W - block_w) // 2, H - margin - block_h
    else:
        x0, y0 = (W - block_w) // 2, (H - block_h) // 2

    sw = int(size * P["sw"])
    # soft shadow
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i, line in enumerate(lines):
        sd.text((x0 + int(size * 0.05), y0 + i * lh + int(size * 0.07)), line, font=font, fill=(0, 0, 0, int(255 * P["shadow"])),
                stroke_width=sw, stroke_fill=(0, 0, 0, int(255 * P["shadow"])))
    sh = sh.filter(ImageFilter.GaussianBlur(max(2, size // 22)))
    im = Image.alpha_composite(im, sh)

    # gradient fill, clipped to the letters
    mask = Image.new("L", im.size, 0)
    md = ImageDraw.Draw(mask)
    for i, line in enumerate(lines):
        md.text((x0, y0 + i * lh), line, font=font, fill=255)
    grad = Image.new("RGBA", im.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    (r1, g1, b1), (r2, g2, b2) = P["fill"]
    for y in range(y0, y0 + block_h + 1):
        t = (y - y0) / max(block_h, 1)
        gd.line([(0, y), (W, y)], fill=(int(r1 + (r2 - r1) * t), int(g1 + (g2 - g1) * t), int(b1 + (b2 - b1) * t), 255))
    d = ImageDraw.Draw(im)
    if sw:
        for i, line in enumerate(lines):
            d.text((x0, y0 + i * lh), line, font=font, fill=P["stroke"], stroke_width=sw, stroke_fill=P["stroke"])
    im.paste(grad, (0, 0), mask)
    im.convert("RGB").save(spec["out"], quality=95)
    print("saved", spec["out"], im.size, "text size", size)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(json.load(open(sys.argv[1], encoding="utf-8")))
