---
name: oyji-marketplace-cards
description: Make marketplace product cards through the OyJI MCP and local text overlay - a compliant main image, secondary product images (angles, detail, lifestyle, what's in the box, infographic) and A+ style content modules - for Kaspi.kz, Satu.kz, Wildberries, Ozon, Amazon and similar listings, with exact Kazakh or Russian text. Use when the user asks for listing images, product detail cards, an infographic, secondary pictures, A+ content or a full image set for a marketplace. For brand or social product photos use oyji-product-photoshoot.
---

# OyJI Marketplace Cards

Adapted from `higgsfield-marketplace-cards` (MIT, (c) 2026 Higgsfield AI): the scopes, the asset list and the delivery rules. Higgsfield keeps its marketplace rules and templates private, so the rules handling, prompts and the text-overlay step below are ours. See `../../NOTICE-higgsfield.md`.

Goal: a set of cards that pass the marketplace's checks, look sales-ready, and never claim anything the seller did not say.

Needs the OyJI MCP (`generate_image`, `upload_from_url`), model `nano-banana-pro`, and local Python with Pillow for text. Images are free.

## First, the rules of the marketplace

Do not guess them. Ask which marketplace and category, and ask the user to paste its current image requirements or open the seller help page. Marketplaces change these rules and differ per category (size, background, how much the product must fill, whether text or badges are allowed on the main image). Safe default when nothing is known: the **main image** is the product alone on a pure white background (#FFFFFF), centred, filling about 85% of the frame, sharp, no text, no logo overlay, no watermark, no props, no people. Say that the default is a default.

## Scopes

| Scope | Creates |
|---|---|
| `main` | 1 main image |
| `product-images` | main + 5 secondary images |
| `aplus` | main + 7 A+ modules |
| `full-set` | main + 5 secondary + 7 A+ modules |

Assets (pick a custom subset if asked):

- Secondary: `infographic`, `multi_angle`, `detail_shot`, `lifestyle`, `whats_in_box`.
- A+ modules: `hero_banner`, `pain_points`, `features`, `ingredients`, `efficacy`, `how_to_use`, `endorsement`.

## What to ask (one short message, at most one question if the rest is clear)

A product photo (strongly preferred: with only text the packaging and printed words cannot be exact), the marketplace and category, the scope, a visual direction or brand colours, and the facts to show: benefits, specs, what is in the box, price and offer if they go on a card. Respond in the user's language (Kazakh or Russian).

## Facts and claims

Use **only** what the user gave you. Never invent benefits, ingredients, certificates, awards, test results, statistics, discounts, "bestseller" labels or reviews. The `efficacy`, `ingredients` and `endorsement` modules are the risky ones: they need the user's own data, and an endorsement is never a made-up quote or a fake person. Regulated categories (food, cosmetics, medicine, children's goods, fertilizers) may need declared wording: if unsure, ask the user for the exact text.

## How each asset is made

All pictures: product photo as image 1 plus the fidelity sentence (`oyji-product-photoshoot`: reproduce shape, colours, logo and every printed word; add no text to the scene). Look at each result against the original and apply the repair ladder from that skill when the product's own text bends.

- `main_image`: white background, product only, 1:1.
- `multi_angle`: front, back, side, top or three-quarter of the same product (the model invents the unseen sides: say so and let the user confirm they match reality).
- `detail_shot`: a macro of one real feature or material, 1:1 or 3:4.
- `lifestyle`: the product in use in a believable place, 1:1 or 3:4.
- `whats_in_box`: a tidy flat lay with **only the items the user listed**.
- `infographic`: a clean base picture (product plus calm empty zones), then **text added locally**.
- A+ modules: 16:9 banners or 3:4 panels, each a clean illustrated base with empty zones; text added locally.

Text is never produced by the image model. Make the base picture with empty areas, then run `scripts/overlay_text.py`:

```json
{"image":"base.png","out":"card.png","position":"bottom",
 "headline":"Органикалық тыңайтқыш","lines":["35 кг · 50 л","Топырақ құнарлылығын арттырады"],
 "badge":"ТЕГІН ЖЕТКІЗУ","footer":"example.kz","color":"#D6B054"}
```

`python3 -I scripts/overlay_text.py spec.json`. It picks a font that has the Kazakh letters and the tenge sign (and stops if none does), draws a gradient behind the text and prints exact words. `position` is `bottom`, `top`, `left` or `right` (left or right suits a wide banner with the product on the other side). Keep infographics to 3 to 5 short points.

Text must not cover the product. Brief the base picture with a clean zone, and pass the product's box as `"avoid": [x0, y0, x1, y1]` (fractions of the picture, from looking at it): the script then tries the other sides and, if none is clear, **stops and tells you to regenerate the base** instead of printing over the label. Tested on a lifestyle picture with the product in the middle (refused) and on a 16:9 banner with the product on the right (text placed on the left).

## Aspect ratios (OyJI offers 1:1, 3:4, 4:3, 9:16, 16:9)

Main and square cards: 1:1. Portrait cards (Wildberries and Ozon often prefer 3:4): 3:4. A+ banners: 16:9. If the marketplace wants an exact size, say that the picture is about 1 to 1.5 thousand pixels and resize or pad it locally; do not stretch.

## Deliver

Reply with the ready picture files in a short list, a label each (main, infographic, lifestyle, ...), and any picture where a rule could not be met or the product text was not exact. No prompts, no internal names unless the user asks.
