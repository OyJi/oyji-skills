---
name: oyji-faceless-video
description: Make a finished narrated "faceless" video through the OyJI MCP - an explainer, documentary, illustrated story or picture story - with one visual style, one narrator voice, scene images, optional motion clips, music and burned-in captions, in Kazakh or Russian. Use when the user asks for a narrated explainer, a story or documentary video, a "faceless" channel video or a picture story. Not for a single silent clip, an ad with a person, or script-only requests.
---

# OyJI Faceless Video

Adapted from `higgsfield-faceless-video` (MIT, (c) 2026 Higgsfield AI): the block plan, the gates and the production order. Tool calls, models, scripts and the Kazakh specifics are ours. See `../../NOTICE-higgsfield.md`.

Goal: one finished video with a consistent look and a narration that fits the picture. An explainer uses deliberate, diagram-led scenes, not rapid cuts. Keep every choice and asset the user supplied.

Needs the OyJI MCP (`generate_image`, `generate_speech`, `list_models`, `get_account`, `upload_from_url`; for motion also `quote_video` and `generate_video`) plus local `ffmpeg`, `ffprobe`, `python3`. Images are free; speech costs a few tenge per line; video clips cost real money (see `oyji-video-director`).

## Before spending anything

Resolve, asking once and briefly: topic or source, length, aspect ratio (9:16 for Reels/Shorts/TikTok, 16:9 for YouTube, 1:1 for the feed), language (Kazakh or Russian), visual style, voice, music (yes/no), captions (yes/no), motion (still pictures with camera moves, or generated clips). Never invent a voice: `list_models` with kind `audio` lists the real voices, including the user's cloned ones. Honour the requested length, never round it up silently. Confirm what a supplied photo is for: a style reference, a character to keep, or something else; never assume.

Check the balance with `get_account`. A still-picture video costs only speech. Motion clips: quote first, say the total, wait for a yes.

## 1. Plan the blocks

- Factual topic: research reliable sources, keep a short source list, and never state a fact you could not source. Personal story: use only the supplied facts.
- One block = one idea = one narration line = one picture, about **10 seconds**; the last block may be shorter. Do not cut a sentence in the middle.
- Kazakh text runs about 9 characters a second including spaces, so a 10-second block holds roughly 80 to 95 characters. Russian is a little denser. These are starting points: the real take decides.
- Save the plan (`plan.json`: blocks, lines, picture descriptions, sources) and keep a ledger of every result URL, so an interruption does not mean regenerating accepted work.

## 2. Style key and roster

- Make one **style key** picture first (`generate_image`, `nano-banana-pro`) and use it as a reference for every scene so the look stays one look. Starting points, not a catalogue: editorial paper collage (cream paper, halftone cut-outs, one accent colour, abstract unlabeled diagrams); paper diorama; cinematic storybook illustration; clay mannequin figures; a children's look (flat 2D, 3D or hand-drawn).
- Recurring characters, places and props get a **roster**: one reference image each, made in the same style, passed as `reference_image_urls` in later scenes. Nano Banana Pro takes six references: style key plus the characters in the scene.
- A real photo given only as a style donor is not copied: no person, logo or composition from it. Do not animate an unmodified real photo as an "illustrated" background.
- Keep readable text out of the pictures: the model bends letters. Words belong in the narration and the captions.
- Look at the first scene before making the rest. Name any defect (wrong aspect, identity drift, flat composition) and redo only the failed pictures.

## 3. Narration

- Pick **one** voice for the whole video. Write natural spoken language, one flowing line per block, no repeated filler.
- `generate_speech` per block. ElevenLabs allows only two requests at once: send them in pairs. Download each take as `voiceNN.mp3` and measure it with `ffprobe`.
- **Timing gate.** A take must land within the block's window (the assembler checks it, default +-35%). Too long or too short: rewrite the line and regenerate. **Never speed the audio up or slow it down.** At most three attempts per line, then tell the user the line does not fit.
- Write numbers and abbreviations as words in the line you send to the voice (digits and abbreviations are read unpredictably), and ask the user to listen to the first take before you generate the rest. You cannot hear it yourself.

## 4. Pictures

One distinct picture per block, in the same style, composed to show what the narrator says at that moment. Vary scale and angle between neighbouring blocks; do not repeat a picture to fill time. Reserve the lower third of the frame for captions. For a sequence that must feel continuous, pass the previous scene's result as a reference and describe only what changes.

## 5. Motion (pick one)

- **Stills with camera moves** (free, the default): the assembler adds a slow push-in or drift to each picture.
- **Generated clips** for the blocks that need real motion: use the scene picture as the first frame, write the shot second by second (`oyji-video-director`), quote and ask first. Generate the voice separately and keep speech out of the clip prompt. Put a clip into the manifest as `"video"` instead of `"image"`: it is trimmed or held on its last frame to match the narration.

## 6. Assemble

`scripts/assemble.py` (Python 3, ffmpeg) turns a manifest into the final file: Ken Burns or generated clip per block, audio joined without changing speed, an optional music bed ducked under the voice, optional burned-in captions made from each block's caption text. Read its docstring for the manifest. Example:

```json
{"out":"final.mp4","aspect":"9:16","window":10,"captions":true,
 "blocks":[{"image":"scene01.png","audio":"voice01.mp3","caption":"Exact words of the line"},
           {"video":"clip02.mp4","audio":"voice02.mp3","caption":"..."}]}
```

Run `python3 -I scripts/assemble.py manifest.json` from the work folder. Captions are timed by block and spread over its characters by default. **Word-exact timing** is optional and runs a local model (nothing leaves the machine):

```bash
~/.oyji-skills-venv/bin/python scripts/word_timing.py voice01.mp3 --text "the exact line" --lang kk --offline --out words01.json
```

then add `"words": "words01.json"` to that block. The script you wrote is the truth for the words; the audio only gives the times, and Kazakh words the model misheard are matched back to the script. It needs `faster-whisper` in its own venv and the model weights; see the README for the one-time setup, and **ask before installing anything or downloading a model**. It uses the first `faster-whisper-*` model it finds in the Hugging Face cache (medium is fine for Kazakh), runs on CPU in about half a minute for a short take, and the script is fed to the model as a prompt, so `matched` only says the times line up, not that the voice said every word: still look at the captions.

## 7. Review before delivering

1. Watch frames at the start, middle and end (extract a strip with ffmpeg and look at it). Check framing, captions legibility, identity drift.
2. Check the length, aspect and audio stream with `ffprobe`; the captions show the exact words of the script.
3. Confirm three statements against the script or sources.
4. Report: actual length, aspect, language, whether captions are burned in, sources, and the total cost (speech plus any clips).

If a gate fails, correct the input and rerun. Do not return loose clips as a finished video.

## 8. Presenter overlay (only when the user asks for one)

A presenter is a talking-head clip from the user's own recording, or a talking character made with `oyji-video-director`. Never infer a presenter from a photo that happens to be in the brief. Then:

```bash
python3 -I scripts/presenter_overlay.py --base final.mp4 --presenter talk.mp4 --out final_presenter.mp4 \
  --position bottom-right --shape circle --size 0.30 --audio presenter
```

It crops the clip to a circle (or rounded square), keeps the corner clear of the caption band, shows the presenter only while their clip plays, and takes their audio, the video's, or a mix. Plan the narration for the blocks where the presenter appears so they are not talking over the voice-over: `--audio mix` is for background music and a presenter, not for two voices.

## 9. Talking characters (only when the user asks for them)

A character that speaks is a short clip per line: the character picture as the first frame, the exact line in quotes with its timing, `oyji-video-director` for the prompt, a quote and a yes first. The mouth is approximate, not frame-exact. Real faces are refused by Seedance (see that skill). Keep each clip within its model's length (Seedance 2.0: 4 to 15 s). Do not combine a generated voice-over and a talking clip in the same block.
