---
name: oyji-websites
description: Design and build a website, landing page or portfolio as a local project (plain HTML/CSS/JS or a Vite + React app) with images, covers and favicons made through the OyJI MCP, a design brief, an SEO and metadata pass and a checklist before handing over. Kazakh, Russian and English content. Use when the user asks for a website, landing page, portfolio or a one-page site. Hosting and publishing are not part of this skill: it builds files and never deploys or publishes anything without an explicit instruction.
---

# OyJI Websites

Adapted from `higgsfield-websites` (MIT, (c) 2026 Higgsfield AI): the intake, the brief-before-code order, the asset system, the mandatory cover and metadata, and the review gate. Higgsfield's version is tied to its own hosting (one Cloudflare Worker per site, `higgsfield website create/deploy/publish`, sign-in with Higgsfield, a games platform). **OyJI has no hosting or publishing platform**, so none of that is here. What remains is the part that does not depend on a platform. See `../../NOTICE-higgsfield.md`.

Needs the OyJI MCP (`generate_image`, `upload_from_url`) for pictures. Images are free; a hero video costs money (`oyji-video-director`).

## What this skill does not do

- It does not host, deploy or publish. The result is a folder. How it goes online (Netlify, Cloudflare Pages, GitHub Pages, a Plesk hosting, a VPS) is the user's choice and an explicit request; never run a deploy, push to a production branch or touch DNS on your own.
- It does not build apps with sign-in, payments or databases by default. If the user wants those, say what is needed (a backend, keys) and ask before choosing.
- No AI generation inside the site for its visitors; the pictures are made once, now, and shipped as files.

## 1. Intake (one compact message)

Ask only what is missing: what the site is for and who visits; language(s) (kk / ru / en, one or several); the pages or sections; brand facts, logo, colours, fonts if they exist (they are fixed constraints; for a new identity use `oyji-brandkit` first); the main action a visitor should take (call, WhatsApp, form, buy); real content to use (texts, prices, contacts, photos); animated or simple (animation costs build time and weight; default to a restrained, fast page); any examples they like (look at them for structure and mood, never copy).

Never invent facts, prices, addresses, phone numbers, testimonials or certificates: use the user's, or leave a clearly marked placeholder and tell them.

## 2. Brief before code

Write a short `brief.md`: purpose, audience, tone, the one primary action, the sections in order with one line each, the palette (hex), type pair (fonts must contain the Kazakh letters ә ғ қ ң ө ұ ү һ і; check as in `oyji-brandkit`), spacing and layout rules, what is deliberately left out. Then build to the brief, not to taste on the day.

## 3. Assets (OyJI MCP)

Make a small consistent asset set instead of random pictures: a hero image, one image per major section, an OG/cover image, and the favicon source. One style across all (palette words and light in every prompt; the first approved picture is a reference for the rest, `nano-banana-pro` takes six).

- Ratios available: 1:1, 3:4, 4:3, 9:16, 16:9. Wide hero 16:9; cards 4:3 or 1:1; mobile hero 9:16 if you want a separate crop.
- Output is roughly 1 to 1.5 thousand pixels on the long side. Fine for a full-width hero on most screens; for a retina full-bleed hero say that it is soft, or place it with a gradient overlay.
- No text inside generated pictures: headlines are HTML. Photographs of people are invented unless the user supplied the person (their own face: `oyji-face-id`).
- Download the images into `assets/`, compress them (`.webp` or `.avif` if tools exist, otherwise optimised JPEG) and write real `alt` text.

## 4. Build

Choose the lightest thing that meets the brief: plain HTML + CSS + a little JS for a landing page; Vite + React only if the site has real interaction. Always: semantic headings (one `h1`), responsive from 360 px, a visible primary action above the fold, a sticky or repeated contact action on mobile, readable contrast, `lang` attribute per language, system-font fallback, no layout shift (set image sizes), `prefers-reduced-motion` respected, keyboard focus visible. Write each file once, complete; do not write then patch.

Multilingual: one folder per language (`/kk/`, `/ru/`, `/en/`) with the same structure and a language switcher, `hreflang` links between them; Kazakh is the default only if the user says so.

## 5. Cover and metadata (always, before handover)

Every site ships with: a 1200 x 630 OG image (a clean picture; text, if any, added locally with `../oyji-marketplace-cards/scripts/overlay_text.py`), `og:title`, `og:description`, `og:image`, a favicon set, `<title>` and meta description per page, a `sitemap.xml` and `robots.txt`, and JSON-LD for a local business or product when the user gave the facts. A site without these is not finished.

## 6. Check before handing over

1. Open it (the Browser pane or a local server) at 360, 768 and 1280 px and look at it.
2. All links and buttons work; the form or contact action really goes where it should; phone and WhatsApp links are right.
3. Every text is the user's text; no placeholder is left unmarked.
4. Images load, sizes are sane (a page over about 3 MB needs a reason), alt text present.
5. Console has no errors; no external script was added without being told.
6. Lighthouse-style basics: title, meta description, one h1, contrast, tap targets.
7. **The subject stays in frame on a phone.** A wide `cover` hero crops the sides on a narrow screen; in a test the product was cut in half at 390 px. Set `background-position` toward the subject (for example `75% center` when it sits on the right), or generate a separate 9:16 crop and swap it with a media query. Look at it at 360 to 390 px every time.

## Deliver

Where the files are, how to open it locally (one command), what is placeholder, which choices were made (fonts, palette), and the options for putting it online. Ask before doing any of that.
