---
name: oyji-video-director
description: Turn finished stills (a character photo, a location) into video through the OyJI MCP: pick the model, write the second-by-second prompt, say what each reference image is for, quote the price, generate, check, and fix. Use after oyji-creature or oyji-location, or whenever the user asks for a short video, ad, animation or shot made from images. Videos cost money, so the user's yes comes before generate_video.
---

# OyJI Video Director

Needs the OyJI MCP (`quote_video`, `generate_video`, `get_media`, `upload_from_url`, `get_account`, `list_models`).

## Money first

Video is paid from the user's tenge balance. Always:
1. `get_account` (balance) and `quote_video` with the exact settings.
2. Tell the user the price and what is left afterwards. If the balance covers one try only, say so and ask whether to use a cheaper setting.
3. Start only after a clear yes in this conversation. A failed video is refunded; a bad result is not.

Rough prices seen on the server (check with `quote_video`, they change): Seedance 2.0, 5 s, 720p about 460 tenge; 480p about 214 tenge.

## Pick the model (`list_models` for the live list)

- **Seedance 2.0** (default): 4 to 15 s, 480p/720p/1080p, up to 9 reference images, first and last frame, audio on or off, ratios 16:9, 9:16, 1:1, 4:3, 3:4, 21:9. Best for animating a still with strong prompts. It refuses photos of real people (error `real_person`): creatures and invented people are fine; for a real face use the account's registered likeness asset or generate the person as an illustration.
- **Kling 3.0 Omni**: changes a *filmed* clip (outfit, product) and keeps the scene, motion and people frame for frame; slow (about 10 minutes for a 10 s edit). Use it for edits, not for making a clip from a still.
- **Veo 3 and Veo 3 Fast**: 4, 6 or 8 s, 16:9 or 9:16 only, 720p or 1080p, **no reference images and no first or last frame**, with sound. Text-to-video only: use it when a clip from a prompt alone is enough.
- Prices per second seen on the server (lowest resolution; `quote_video` is the truth): Seedance 2.0 about 43 tenge, Kling 3.0 Omni about 69, Veo 3 Fast about 90, Veo 3 about 240.
- **Seedance edit mode** rewrites the whole clip instead of editing it in place. Do not use it to "change one thing".
- Seedance 2.5 (4K, true draft-then-final) is not open on OyJI yet. Until it is, do not promise 4K.

## References: what each image is for

- Name the images in order (`@image1`, `@image2`) and give each one job. Example: image 1 the character, image 2 the place.
- Tell it what to take and what to drop: `From image 2 take only the place.` / `Do not take the character photo's wall, floor, flash lighting, hard shadow or pose.`
- One image can instead be the **first frame** (`first_frame_url`), optionally with a **last frame** (`last_frame_url`) so the clip ends exactly where you want. References and frames are different inputs: use one or the other.
- Every URL must come from `upload_from_url` or an earlier OyJI result. A local file has to be on a public link first (any host you control or a public bucket); then `upload_from_url`.

## The prompt, written second by second

Describe the shot like a director, not like a tag list:

1. **Format and length in the first line**: `5 seconds, vertical 9:16, one continuous take, no cuts` (or list shots with their seconds).
2. **Camera**: its start position, its move (a slow push in, a swing around to the door and back), its speed. If you want a locked camera, say `static locked-off camera, no movement`.
3. **Action by second**: `0-2 s: he stands still and lifts his head; 2-4 s: he looks at his hands; 4-5 s: he turns toward the door.`
4. **Light and place** from the location reference.
5. **Sound** if audio is on: ambience, steps, breath, one spoken line in quotes.
6. **What must not change**: `The creature's design, costume and face stay identical in every frame.`
7. End with the negatives: no subtitles, no captions, no extra characters, no new objects, no morphing.

Moving objects "pop" in and out cleanly if you write `old objects pop out, new objects pop in; nothing morphs into anything else`.

## Speech and lip sync

The model moves the mouth roughly, not exactly. Put the exact line in quotes with its timing (`starts at 0.3 s, ends by 4.5 s, then closes the mouth`), keep it short (about 2.3 syllables a second). Real dubbing is done in post. `generate_speech` makes the voice (ElevenLabs allows only two requests at once: send them in pairs).

## Text in the picture

Video models bend small text: package captions, screens, signs turn into nonsense while the clip moves. Do not rely on the model for readable text. Keep the shot free of text and add titles, prices and logos in editing (OyJI Studio or ffmpeg). If a package must stay readable, re-draw those regions from the clean still on every frame instead of trusting the render.

## Cheap check, then the real one

True draft-then-final is not available on OyJI yet, and a second run is a *different* take. So: write the prompt well, run once at the resolution the user can afford, and look at the frames (extract a strip with ffmpeg and view it) before spending more. If a take is good, do not re-roll it.

## Check the result

1. Does the character keep its design in the last frame as in the first?
2. Do textures hold when it moves (fur, scales, felt), or do they melt?
3. Is the camera doing what was written?
4. Did the place appear without borrowed walls, floor or light from the character photo?
5. Was any text distorted? Plan to cover it in post.
6. Is the end frame clean enough to cut into the next shot?

If it fails, change one thing in the prompt (usually a clearer "take only X from image N", or a calmer camera) and say what you changed.

## Making a longer piece

Chain clips: clip n starts from the last frame of clip n-1 (`first_frame_url`) and ends on a prepared frame (`last_frame_url`); trim the duplicated last frame when joining. Generate the frames as free stills first, settle the look there, and pay only for the clips.
