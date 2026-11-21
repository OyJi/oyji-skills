#!/usr/bin/env python3
"""Put exact text on a picture: a headline, short info lines, a badge, a small footer.

Image models bend letters (Kazakh ә ғ қ ң ө ү ұ і and the tenge sign ₸ most of all), so
titles, prices and benefits are always added here, never asked of the image model.

    python3 overlay_text.py spec.json

spec.json:
{
  "image": "card.png",            # input picture
  "out": "card_text.png",
  "position": "bottom",           # "bottom" | "top" | "left" | "right": where the text block goes
  "avoid": [0.18, 0.25, 0.54, 0.77],  # optional box (x0, y0, x1, y1 as fractions) the text must not touch,
                                  # e.g. the product; the script tries the other sides and stops if none is clear
  "headline": "Органикалық тыңайтқыш",
  "lines": ["3 000 ₸ / қап", "10 қаптан бастап жеткізу тегін"],
  "badge": "ТЕГІН ЖЕТКІЗУ",       # optional pill in the corner
  "footer": "example.kz",         # optional small line
  "color": "#D6B054",             # accent colour (badge, rule)
  "text_color": "#FFFFFF",
  "scrim": 0.62                   # 0..1 darkness of the gradient behind the text
}

Run with `python3 -I`. Needs Pillow. The font is searched on this machine and must contain
the Kazakh letters and ₸ (checked below); if none does the script stops instead of printing boxes.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

NEED = "ӘәІіҢңҒғҮүҰұҚқӨөҺһ₸"
FONT_CANDIDATES = [  # (bold, regular) pairs, with the face index inside a .ttc
    ("/System/Library/Fonts/Helvetica.ttc", 1, "/System/Library/Fonts/Helvetica.ttc", 0),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0, "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 0),
    ("C:/Windows/Fonts/arialbd.ttf", 0, "C:/Windows/Fonts/arial.ttf", 0),
]


def covers(path, index):
    try:
        from fontTools.ttLib import TTFont, TTCollection
        f = TTCollection(path).fonts[index] if path.endswith(".ttc") else TTFont(path)
        cmap = f.getBestCmap()
        return all(ord(c) in cmap for c in NEED)
    except Exception:
        return True  # fontTools missing: trust the candidate list, check the picture afterwards


def pick_fonts():
    for bpath, bi, rpath, ri in FONT_CANDIDATES:
        if os.path.exists(bpath) and os.path.exists(rpath) and covers(bpath, bi) and covers(rpath, ri):
            return (lambda s: ImageFont.truetype(bpath, s, index=bi)), (lambda s: ImageFont.truetype(rpath, s, index=ri))
    sys.exit("No font with Kazakh letters and the tenge sign found; install DejaVu Sans or Noto Sans.")


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def layout(draw, spec, W, H, pos, bold, regular, accent, fg):
    """Measure the text block for a position and return everything needed to draw it."""
    pad = int(W * 0.06)
    head_size = max(28, int(W * 0.07))
    line_size = max(20, int(W * 0.04))
    foot_size = max(16, int(W * 0.028))
    side = pos in ("left", "right")
    if side:  # a narrower column for a banner with the product on the other side
        head_size, line_size, foot_size = int(head_size * 0.8), int(line_size * 0.8), int(foot_size * 0.9)
    max_w = int(W * 0.5) - pad if side else W - 2 * pad
    blocks = []  # (text lines, font, colour, gap after)
    if spec.get("headline"):
        blocks.append((wrap(draw, spec["headline"], bold(head_size), max_w), bold(head_size), fg, int(head_size * 0.35)))
    for t in spec.get("lines", []):
        blocks.append((wrap(draw, t, regular(line_size), max_w), regular(line_size), fg, int(line_size * 0.3)))
    if spec.get("footer"):
        blocks.append(([spec["footer"]], regular(foot_size), accent, 0))
    heights = [int(f.size * 1.2) * len(lines) + gap for lines, f, _, gap in blocks]
    total = sum(heights) + (int(head_size * 0.5) if spec.get("headline") else 0)
    widest = max((int(draw.textlength(l, font=f)) for lines, f, _, _ in blocks for l in lines), default=0)
    if side:
        band_w = min(int(W * 0.5), widest + 2 * pad)
        y0 = max(pad, (H - total) // 2)
        x0 = pad if pos == "left" else W - band_w + pad
        rect = (0 if pos == "left" else W - band_w, y0 - pad, band_w if pos == "left" else W, y0 + total + pad)
    else:
        band = total + 2 * pad
        y0 = pad if pos == "top" else H - band + pad
        x0 = pad
        rect = (0, 0 if pos == "top" else H - band, W, band if pos == "top" else H)
    return dict(blocks=blocks, heights=heights, head_size=head_size, pad=pad, x0=x0, y0=y0, rect=rect, total=total, side=side, pos=pos)


def hits(rect, avoid, W, H):
    ax0, ay0, ax1, ay1 = avoid[0] * W, avoid[1] * H, avoid[2] * W, avoid[3] * H
    x0, y0, x1, y1 = rect
    return not (x1 <= ax0 or x0 >= ax1 or y1 <= ay0 or y0 >= ay1)


def main(spec):
    bold, regular = pick_fonts()
    im = Image.open(spec["image"]).convert("RGB")
    W, H = im.size
    accent = hex_rgb(spec.get("color", "#D6B054"))
    fg = hex_rgb(spec.get("text_color", "#FFFFFF"))
    d0 = ImageDraw.Draw(im)

    want = spec.get("position", "bottom")
    order = [want] + [p for p in ("bottom", "top", "left", "right") if p != want]
    L = None
    for pos in order:
        cand = layout(d0, spec, W, H, pos, bold, regular, accent, fg)
        if not spec.get("avoid") or not hits(cand["rect"], spec["avoid"], W, H):
            L = cand
            break
    if L is None:
        sys.exit("The text would cover the protected area on every side. Regenerate the base picture with a clean zone "
                 "(for example the top or bottom third left empty) instead of printing over the product.")
    if L["pos"] != want:
        print("note: moved the text from %s to %s to stay off the protected area" % (want, L["pos"]))

    top = L["pos"] == "top"
    rx0, ry0, rx1, ry1 = L["rect"]
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    alpha_max = int(255 * float(spec.get("scrim", 0.62)))
    if L["side"]:
        span = rx1 - rx0
        for i in range(span):
            t = (1 - i / span) if L["pos"] == "left" else (i / span)
            sd.line([(rx0 + i, 0), (rx0 + i, H)], fill=(0, 0, 0, int(alpha_max * (t ** 1.3))))
    else:
        band = ry1 - ry0
        for i in range(band):
            t = (band - i) / band if top else i / band
            sd.line([(0, ry0 + i), (W, ry0 + i)], fill=(0, 0, 0, int(alpha_max * (t ** 1.3))))
    im = Image.alpha_composite(im.convert("RGBA"), scrim)
    d = ImageDraw.Draw(im)

    y = L["y0"]
    first = True
    for (lines, font, colour, gap), h in zip(L["blocks"], L["heights"]):
        for ln in lines:
            d.text((L["x0"], y), ln, font=font, fill=colour)
            y += int(font.size * 1.2)
        y += gap
        if first and spec.get("headline"):
            d.rounded_rectangle((L["x0"], y, L["x0"] + int(W * 0.12), y + max(4, int(W * 0.006))), radius=3, fill=accent)
            y += int(L["head_size"] * 0.5)
        first = False

    if spec.get("badge"):
        pad = L["pad"]
        f = bold(max(18, int(W * 0.032)))
        tw = d.textlength(spec["badge"], font=f)
        bx1 = W - pad
        by1 = pad if not (top or L["pos"] == "right" and False) else H - pad - int(f.size * 2)
        if L["pos"] == "right":
            bx1 = int(W * 0.5) - pad  # keep the badge off the text column on the right
        bx0, by0 = bx1 - tw - 2 * int(f.size * 0.7), by1 + int(f.size * 2)
        d.rounded_rectangle((bx0, by1, bx1, by0), radius=int(f.size), fill=accent)
        d.text((bx0 + int(f.size * 0.7), by1 + int(f.size * 0.45)), spec["badge"], font=f, fill=(20, 40, 28))

    im.convert("RGB").save(spec["out"], quality=95)
    print("saved", spec["out"], im.size, "text at", L["pos"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(json.load(open(sys.argv[1], encoding="utf-8")))
