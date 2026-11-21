---
name: oyji-thumbnail
description: Make high-click-through YouTube thumbnails and vertical video covers (Shorts, Reels, TikTok) through the OyJI MCP - a truthful information-gap concept, up to three identities from the user's own photos, an optional logo, variants, and a crisp headline added locally in Kazakh or Russian. Use when the user asks for a thumbnail, a video cover, a Shorts or Reels cover, or "a cover for this video". Chain after a video workflow once the topic is known. Not for the video itself, product photos or marketplace cards.
---

# OyJI Thumbnail

Adapted from `higgsfield-youtube-thumbnail` (MIT, (c) 2026 Higgsfield AI): the concept gate, the reference manifest, the prompt order, the post-render gate and surgical tweaks. Tools, models and the text overlay are ours. See `../../NOTICE-higgsfield.md`.

Needs the OyJI MCP (`generate_image`, `upload_from_url`), model `nano-banana-pro`, and local Python with Pillow for the headline (`scripts/thumb_text.py`). Images are free.

## Rules

1. Respond in the user's language. Keep the model mechanics out of the chat.
2. **Truth.** The thumbnail may only promise what the video really delivers. Never invent claims, results, products, people, screenshots or numbers.
3. A style-reference thumbnail is for looking at (energy, framing, palette, emotion) and is **never** passed to the model as a reference image: copying its identity or exact layout is not allowed.
4. Ask only what the brief does not answer, in one compact question: the video's topic and promise, who appears (0 to 3 people), a logo, a headline (2 to 4 words), the ratio.
5. If a concept needs a person and no face photo was given, ask whether to use the user (their face profile, see `oyji-face-id`), another provided person (with their permission), or an invented character. Never choose silently.

## Ratios (OyJI: 1:1, 3:4, 4:3, 9:16, 16:9)

16:9 for YouTube; 9:16 for Shorts, Reels and TikTok (faces in the upper two thirds, the bottom is covered by the app's own buttons); 3:4 for an Instagram feed cover (OyJI has no 4:5). The picture comes at roughly 1 to 1.5 thousand pixels on the long side: enough for these uses; say so if 4K is asked.

## Concept gate

Think of at least five truthful concepts internally and pick the strongest. Prefer one focal subject, minimal clutter, and an **information gap**: the viewer sees something that makes them need the answer, and the video gives it. Useful frames: a reaction face next to the one surprising object; a huge scale contrast; a number or result that begs "how"; a before/after (only when asked); a mystery object partly hidden; a versus (a split layout only if asked); a person pointing at nothing is **not** a concept. It must read in under a second at about 120 px wide: check by shrinking the result to 120 px and looking at it.

Emotion ladder when the user gives only a count: shock, hype, anger, awe, laughter, fear, smugness, charisma, confusion, determination, disgust.

## References and the prompt

Reference order: faces first (character order), then the logo, at most 6 in all (`nano-banana-pro`). When two or more are attached, the first line of the prompt names them: `IMAGE REFERENCES: image 1 = CHARACTER 1 face; image 2 = brand logo.`

Prompt order (our wording):
1. **Frame:** a bold, punchy, poster-grade photoreal thumbnail, the chosen ratio, one unified frame (no split-screen unless asked).
2. **Scene:** exactly the content the user described.
3. **Text:** default `No text, no readable UI labels, no watermark.` The headline is added afterwards (below).
4. **People:** large, foreground, chest-up or medium close, about 40 to 60% of the frame; `All faces crisply sharp.` For each referenced person: `CHARACTER N: the person from image K, exactly the same face: bone structure, eye shape, nose, lips, jaw, skin tone, hairline. Do not beautify, average or restyle. Expression: <emotion>.`
5. **Key elements:** only the props that explain the gap.
6. **Logo:** exact shapes, colours and letters, away from faces. (A glossy 3D logo is a separate image first; use it as the last reference.)
7. **Place, composition:** one hero at a power third, clear scale hierarchy, strong subject-background separation.
8. **Background:** a vivid high-contrast colour field or environment with a soft vignette.
9. **Light on people:** a strong key light sculpting the face, a soft fill, and a bright rim light tracing the hair and shoulders.
10. **Grade:** vivid, glossy, poster-punchy, deep blacks; restrain only for an explicit calm or premium brief.

Make one call per distinct concept or expression (`count` 1 to 2 is fine); vary only the concept, expression or camera line. Cap the whole job at about 16 generations.

## Check every result (look at it)

Identity matches the references; no stray text or watermark; the face and the hero element still read at 120 px; the concept is true to the video. A hard failure: rerun the same prompt at most twice. If you cannot view the image, say so and let the user judge; do not claim it passed.

## Surgical tweaks

Use the picked result as the only reference and `strict: true`: `Change ONLY <the expression / the background colour / the rim light>. Everything else stays exactly as it is.` Allowed scopes: expression, background replacement, background recolour, rim-light recolour. Never regenerate the whole picture for a small request.

## The headline (local, never from the model)

`python3 -I scripts/thumb_text.py spec.json`, one headline of 2 to 4 words, in Kazakh or Russian. Presets: `beast` (yellow, thick black stroke), `fire` (orange to red), `lime` (neon lime), `clean` (white with soft shadow).

```json
{"image":"pick.png","out":"thumb.png","text":"БҰЛ НЕ БОЛДЫ?","preset":"beast","position":"left","size":0.16}
```

`position`: `left`, `right`, `top`, `bottom`, `center`. Keep text off the face; if the base picture has no free area, regenerate the base with a clear zone instead of covering the subject. The script uses a font that has the Kazakh letters and stops if none does.

## Deliver

The passing pictures with a short label each (for example `shock / close-up`), the ratio, and whether each is clean or has the headline. No prompts or IDs unless asked.
