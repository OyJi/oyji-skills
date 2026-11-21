---
name: oyji-product-photoshoot
description: Make brand-quality product pictures from a product photo through the OyJI MCP (image generation is free) - studio shots, lifestyle scenes, close-ups with hands, hero banners, social carousels, ad packs, virtual try-on, conceptual and restyled versions - keeping the product, its logo and its printed text faithful. Use when the user asks for a product photo, studio or lifestyle shot, banner, carousel, ad creative, "model wearing it" or a new look for an existing product image. For marketplace listing cards use oyji-marketplace-cards.
---

# OyJI Product Photoshoot

Adapted from `higgsfield-product-photoshoot` (MIT, (c) 2026 Higgsfield AI): the modes, the mode-selection rules and the short interview. Higgsfield keeps its prompt templates on a private server, so the templates and the fidelity workflow below are ours. See `../../NOTICE-higgsfield.md`.

Goal: pictures a brand can post, with **the product itself unchanged**: shape, colours, logo and every printed word.

Needs the OyJI MCP (`generate_image`, `upload_from_url`). Model `nano-banana-pro`. Images are free, so make variants.

## Tool facts (verified on OyJI)

- `reference_image_urls`: up to **6** with `nano-banana-pro` (3 with `nano-banana`). The product photo is always image 1.
- `count` up to 4 results per call. `strict: true` changes only what the prompt names.
- Ratios available: **1:1, 3:4, 4:3, 9:16, 16:9**. Map the usual asks: 4:5 and 2:3 become 3:4; vertical Story or Reel is 9:16.
- Output is roughly 1 to 1.5 thousand pixels on the long side. Fine for Instagram, Threads, WhatsApp and most marketplaces; say so if the user needs print or a huge banner.
- A file on the user's disk must first be a public URL, then `upload_from_url`.

## Modes

| Mode | When the user wants |
|---|---|
| `product_shot` | the product on a clean studio or catalogue background |
| `lifestyle_scene` | the product in real life: a kitchen, a field, a cafe, in a hand |
| `closeup_with_person` | a tight crop with hands or part of a face: applying, holding, showing |
| `vertical_story` | a 9:16 or 3:4 poster-like picture for Stories, Reels covers, Pinterest-style pins |
| `hero_banner` | a wide 16:9 header for a site, email or campaign |
| `social_carousel` | 3 to 10 connected slides |
| `ad_creative_pack` | a coordinated set of static ad variants |
| `virtual_try_on` | the product worn or used by an invented model |
| `conceptual_product` | surreal, floating, splashing, sculptural |
| `restyle` | a new mood or season for an existing image without changing the subject |

Pick by intent, not by a keyword; when two fit, the more specific wins (platform format beats scene, multi-slide beats scene, a named genre beats the general one).

## Interview (at most 4 short questions, labelled options, skip what is obvious)

- Product photo uploaded, "make me pictures": how many (1 / 3 / 5), style (clean studio / lifestyle / conceptual / with a model), where it will be used (Instagram / Kaspi, Satu / ads / site), brand colours.
- Photo plus a clear use ("a banner", "ads"): ask only what is missing: the offer or hook, the number of variants, what to emphasise.
- No photo: ask for one first (much higher fidelity); if impossible, ask for category, packaging, colours and distinctive features, and warn that printed text will not be exact.
- Existing picture to change: the aesthetic, the season, and what must stay.

## Prompt skeleton (ours)

```
Image 1 is the product reference: reproduce the product exactly: shape, proportions, colours, material, logo and every printed word and number. Do not redesign, simplify, translate or rename it.
<MODE BLOCK: scene, light, camera, composition>
<Palette and mood in plain words>
Add no text, logo, watermark or price anywhere in the picture except what is printed on the product itself.
```

Mode blocks:

- **product_shot**: seamless pale grey or white sweep, large soft light from one side, a soft contact shadow, 85 mm look, product centred and filling about 70% of the frame.
- **lifestyle_scene**: a plausible real place for this product, natural window or daylight, sparse props that belong to it, depth of field, the product label facing the camera and in focus.
- **closeup_with_person**: tight crop, an invented adult (hands or part of a face), the product label readable and facing the camera, natural skin.
- **vertical_story**: 9:16, product in the lower two thirds, the top third left clean for a headline added later.
- **hero_banner**: 16:9, product on one third, calm negative space on the rest for text added later.
- **social_carousel**: one locked visual system (same palette, backdrop, light, lens) across slides; slide 1 a hook, middle slides one idea each with varied crops, the last slide a call to action area left clean. Generate slides in one conversation, passing the first approved slide as a reference.
- **ad_creative_pack**: 3 to 5 variants with different angles of attack (benefit, offer, social proof, season), different compositions, same product and brand colours; text is added afterwards.
- **virtual_try_on**: image 1 the garment or product, an invented model of the requested type, full body or three quarters, the item shown clearly; do not alter the garment. For the user's own face, use the OyJI face-profile tools and only after they confirm the photos are of themselves.
- **conceptual_product**: floating, splash or sculptural composition, physically plausible, the product still readable.
- **restyle**: `strict: true`, "keep the subject, pose and layout; change only the aesthetic or season".

Variants must really differ (preset, light, angle, palette). Do not paste the assembled prompt back to the user: they want the pictures.

## Keep the product faithful (in this order)

1. Product photo as image 1, `strict: false` for new scenes (the model must be free to build the scene), the fidelity sentence at the top of the prompt.
2. Look at every result next to the original. Check silhouette, colours, logo, **printed text**. Image models bend small print.
3. If the label text is wrong: fewer scene elements and a closer product; rerun once.
4. Still wrong: repair that region from the original photo (crop the original label, align it to the result and blend it in with Pillow or OpenCV, as was done for a test pack), or place the original product on a generated background.
5. Text that is not on the product (price, headline, offer) is never made by the model: add it with `../oyji-marketplace-cards/scripts/overlay_text.py`.

## Deliver

List the pictures with a short label each (mode, ratio). Say what needs text added and offer to do it. Report any picture where the product text could not be kept exact.
