---
name: oyji-brandkit
description: Build or extend a visual brand system through the OyJI MCP and local tools - palette, logo concepts, typography with Kazakh letters, mockups, social graphics, packaging, posters and a one-file brand sheet or PDF - while keeping the user's official assets fixed and getting approval at each foundation step. Use when the user asks for a brand kit, visual identity, logo, brandbook, or to apply an existing logo to branded materials. Not for unbranded image generation, product catalogue photos (oyji-product-photoshoot) or building a website.
---

# OyJI Brandkit

Adapted from `higgsfield-brandkit` (MIT, (c) 2026 Higgsfield AI): the Brand Lock, the palette-logo-typography approval sequence, the dependency rules and the QA gates. Higgsfield's version relies on its vector model, a 56 KB Python state tool and a PPTX builder; this one uses only OyJI image generation and light local tools, and says plainly what it cannot do. See `../../NOTICE-higgsfield.md`.

Treat the user's brand facts and official assets as **fixed constraints**.

Needs the OyJI MCP (`generate_image`, `upload_from_url`), local Python with Pillow. Images are free.

## What OyJI cannot do (say it, do not fake it)

- **No vector logo model.** `nano-banana-pro` makes raster concepts. A real SVG needs one of: (a) trace the chosen raster with a local tool such as `potrace` or `vtracer` (ask before installing anything), (b) a simple geometric mark written by hand as SVG, labelled as an approximation to be refined by a designer. Never call a raster file "editable" or "vector".
- No Figma, Canva, PSD, AI or EPS files.
- Image models bend text. Wordmarks, slogans and any copy are set locally (fonts), never taken from the model.

## Behaviour

- Match the user's language. Keep your art-direction reasoning private; show results.
- Ask one compact set of only the questions that block progress. Do not run a full identity questionnaire for a partial task.
- After each palette, logo, typography or application review, stop and wait for the user's reply. Never infer approval from silence or from liking the picture yourself.
- Preserve exact user copy. Never invent positioning, values, claims, prices, certificates or statistics.

## 1. Classify the request

- **apply-existing**: the user has an official logo, colours, fonts: apply them, do not redesign them.
- **extend-partial**: make only the missing pieces the requested output needs.
- **create-identity**: design a new identity only when explicitly asked.

## 2. Brand Lock

Write `brand/lock.json` (state lives in the folder, not in your memory): exact brand name spelling and script, official assets (file paths), colours (hex), fonts by role, layout and shape rules, requested outputs, forbidden treatments. Copy the same values into every related generation prompt. Foundation slots required per output: logo-only needs palette + logo (or the official logo alone); text-bearing social, packaging, posters need logo + palette + typography; a brand sheet needs all three.

Record approvals in `brand/approved.json` with what each depended on (palette version, logo file). A changed palette invalidates a logo made from it and what follows; a changed font does not invalidate the symbol mark. Never edit approvals by hand to skip a step.

## 3. New identity, in this order

1. **Palette**: show 2 or 3 palettes as rendered swatch sheets (Pillow, exact hex, a name and a role for each colour). Wait. Save the chosen one.
2. **Logo concepts**: three clearly different symbol ideas (one idea each: a shape logic, not three variations of one). Generate each with `nano-banana-pro`: a flat symbol on a plain light background, no text, no shading, no mockup, 1:1, 2 takes each. Show them, wait for a choice. Vectorise only the chosen one (see above), keep the original file, inspect the result at small size (32 px) and in one colour.
3. **Typography**: 2 or 3 display + body pairs, rendered with the real brand name and a sample line **in Kazakh**. A font must contain ә ғ қ ң ө ұ ү һ і and, if prices appear, ₸. Check before proposing:

   ```bash
   python3 -I -c "
   from fontTools.ttLib import TTFont
   f=TTFont('FONT.ttf'); cm=f.getBestCmap()
   print([c for c in 'ӘәІіҢңҒғҮүҰұҚқӨөҺһ₸' if ord(c) not in cm])"
   ```

   Empty list means it passes. Noto Sans, Roboto, PT Sans, Inter and Montserrat are usual candidates; verify the exact files you will ship. Wait for a choice.

## 4. Applications (load only what was asked)

Mockups, social graphics, posters or banners, packaging, signage, merchandise, a presentation. For each:

- Photoreal mockup: generate the scene with the approved logo as a reference (`reference_image_urls`), with the logo kept to the same shape and colours. Check the logo against the original; if the model bent it, place the real logo file onto the mockup locally instead.
- Anything with copy: base picture from the model, text set locally with the approved font (`../oyji-marketplace-cards/scripts/overlay_text.py` for simple cases, Pillow for layouts).
- Use the same approved logo file everywhere; do not redraw it.

## 5. Brand sheet

One self-contained HTML file in `brand/`: logo (colour, one-colour, small), clear space rule, palette with hex and roles, type pairs with Kazakh sample text, a few correct and incorrect uses, the applications made. Render a PDF with headless Chrome (`--headless --print-to-pdf`) or the Browser pane. Warn that the fonts must be installed to edit it. Do not produce a PowerPoint by improvisation; if the user needs PPTX, ask before installing `python-pptx`.

## 6. QA

Before showing: spelling of the brand name and all copy; logo equals the approved file; colours match the hex values; the font is the approved one and the Kazakh letters render; legibility at small size; nothing invented. Repair only the failing output. Retry a failed generation once with the same locked concept; after the second equivalent failure, stop and report the real error.

## Deliver

The requested files with previews, a short Brand Lock summary, a clear label for each file (vector, raster, editable HTML), any font or import limitation, and stable names for targeted revisions.
