# oyji-skills

Skills for Claude Code (and other agents that load Markdown skills) that make realistic AI images, video and content through the **OyJI MCP** (https://oyji.org). Eleven skills: creatures and locations, product photoshoots, marketplace cards (Kaspi, Satu, Wildberries, Ozon), narrated faceless video, thumbnails, websites, brand kits, your own face as a character, and an entry point that routes a plain request to the right one. Text and examples are Kazakh, Russian and English.

> Қысқаша: бұл OyJI MCP арқылы шынайы сурет, видео және контент жасайтын Claude Code skill-дері. Орнату: төмендегі екі команда. OyJI аккаунты мен MCP кілті керек (oyji.org, Профиль, "Claude Code and Codex (MCP)").

## What you need

- Claude Code.
- An account on https://oyji.org and an MCP key (Profile, "Claude Code and Codex (MCP)"). Images are free; **videos cost money** and every skill asks you before it spends anything (it quotes the price first); speech costs a few tenge.
- For the helper scripts: `ffmpeg` and Python 3 with `Pillow` (and `opencv-python` for some repairs). Fonts are not bundled: the scripts use fonts already on your computer and say so when a font lacks Kazakh letters.

## Install in Claude Code

```text
/plugin marketplace add OyJi/oyji-skills
/plugin install oyji-skills@oyji
```

Then connect the OyJI MCP with your own key. The Profile page shows the exact command with your key filled in; it looks like this:

```bash
claude mcp add --transport http oyji https://oyji-server-tcgnnjlpuq-uc.a.run.app/api/v1/mcp \
  --header "Authorization: Bearer oyji_sk_..."
```

Keep the key private: anyone who has it can spend your balance. Revoke it on the same page if it leaks.

### Without the plugin system (other agents, Codex)

Copy the folders from `plugins/oyji-skills/skills/` to where your agent loads skills (for Claude Code: `~/.claude/skills/`) and keep `NOTICE-higgsfield.md` next to them. Connect the MCP in your agent's own way (the Profile page has a Codex snippet too).

## The skills

| Skill | What it does |
|---|---|
| `oyji-generate` | The entry point: which tool or model for a plain request, money rules, errors, routing to the other skills |
| `oyji-creature` | Photoreal creatures, hybrids, mythic beings: clay shape, real face/animal donor, material swatches, one plain flash photo |
| `oyji-location` | Empty rooms and places that look photographed, used as the setting for a video |
| `oyji-video-director` | Turn stills into video: model choice, price check, second-by-second prompt, reference jobs, result check |
| `oyji-product-photoshoot` | Brand product pictures from a product photo (10 modes), keeping the product and its printed text faithful |
| `oyji-marketplace-cards` | Listing cards for Kaspi, Satu, Wildberries, Ozon: main image, secondary images, A+ modules, exact Kazakh/Russian text via `scripts/overlay_text.py` |
| `oyji-faceless-video` | Narrated faceless video (explainer, story, documentary): style key, voice, timing gate, `scripts/assemble.py` (Ken Burns, music, captions), `word_timing.py` (word-exact captions), `presenter_overlay.py` |
| `oyji-face-id` | Your own face profile: consent, photo checklist, drawing you as a character, deleting |
| `oyji-thumbnail` | YouTube/Shorts/Reels covers: truthful concepts, variants, headline via `scripts/thumb_text.py` |
| `oyji-websites` | Sites and landing pages as local projects with OyJI assets, cover and metadata; it never hosts or publishes anything |
| `oyji-brandkit` | Palette, logo concepts, Kazakh-ready typography, applications and a brand sheet, with approvals and honest limits (no vector model) |

Ask for what you want in plain words ("make a cover for my video about ...", "product photos of this tea pack"); `oyji-generate` picks the skill.

### Optional: word-exact captions

`oyji-faceless-video` can time captions to the spoken words with a local speech-to-text model:

```bash
python3 -m venv ~/.oyji-skills-venv
~/.oyji-skills-venv/bin/pip install faster-whisper "av>=14,<17"   # av 17+ breaks faster-whisper 1.2
```

About 220 MB, plus a `faster-whisper-*` model folder in `~/.cache/huggingface/hub`, or let the script download one (omit `--offline`). Without it captions are timed per block.

## Rules the skills follow

- No voice or face of a real person is cloned or drawn without the owner's consent; the face-profile skill only takes your own photos.
- Prices are shown before any paid step and nothing paid starts without your yes.
- Texts on products, prices and headlines are placed by scripts, never invented by an image model; Kazakh letters are checked in every font.
- When OyJI has no tool for something (3D, vector logos, music, hosting) the skill says so instead of faking it.

## Where the ideas come from

The staged method for realistic characters (clay, face donor, material swatches, plain flash photo, locations without clay, second-by-second video prompts, cheap draft before the final) is described in the public Higgsfield tutorial by Adil, https://www.youtube.com/watch?v=FRukXPBqlNo. The text of `oyji-creature`, `oyji-location` and `oyji-video-director` is our own. Eight other skills are **adapted** from Higgsfield's official skills repo (https://github.com/higgsfield-ai/skills, MIT, (c) 2026 Higgsfield AI): the workflow structure is theirs; the tools, prompt templates, scripts and the market are ours. The licence and attribution are in `NOTICE-higgsfield.md`; keep that file with any copy.

## Not built yet

- Draft-then-final (480p draft, finalise the same take in 1080p/4K) needs a model that supports it on OyJI.
- 3D, GIF/SVG output, virality scoring, music and song videos, hosting and publishing for sites: OyJI has no such tools.
- Brandkit: no vector logo model, no PPTX builder.

## Licence

MIT, (c) 2026 OyJI, see `LICENSE`. Parts adapted from Higgsfield skills are under their MIT licence, see `NOTICE-higgsfield.md`.

Issues and ideas: open an issue in this repository or write through https://oyji.org.
