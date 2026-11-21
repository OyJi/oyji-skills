---
name: oyji-face-id
description: Set up and use the user's own OyJI face profile so generated pictures keep their identity - consent, photo checklist, adding photos (links or files from the user's machine), the profile status, drawing the user as a character or in a new look, and deleting the profile. Use when the user wants their own face in generated images ("make me a character", "photos of me in...", "set up my face", "digital twin"), or asks to check or delete their face profile. Own photos only, adults only.
---

# OyJI Face ID

Adapted from `higgsfield-soul-id` (MIT, (c) 2026 Higgsfield AI): the one-time setup, then reuse pattern. Higgsfield trains a model; OyJI keeps checked photos and uses them as references, so the tools, rules and limits below are ours. See `../../NOTICE-higgsfield.md`.

Needs the OyJI MCP: `get_face_profile`, `face_profile_consent`, `add_face_photo`, `create_face_profile`, `delete_face_photo`, `delete_face_profile`, `make_character`, `list_character_styles`.

## Rules that never bend

Face photos are biometric data.
- **Own face only.** Pass `own_face: true` and `adult: true` **only after the user told you in this conversation** that the photos are of themselves and that they are 18 or older. Never assume it, never infer it from a file name, never use someone else's photo, a celebrity's, or a photo "with permission" in this profile.
- Someone else's face for a character (a friend, a family member, a client): that is not this skill. `make_character` with `consent: true` is allowed only if the user says the photo is theirs or the person gave permission; say what you were told.
- Never show, print or move the stored photos: the profile tools never return them, and you must not try to get them out.
- Deleting is permanent: ask first, then `delete_face_profile` with `confirm: true`.

## 1. Check what exists

`get_face_profile`: whether consent is on, how many photos of each kind (`face`, `half`, `full`) are kept, whether it is ready, and what is missing. Tell the user in plain words ("ready", or "I need 3 more close-ups and 1 full-length"). Do not start over if a profile exists.

## 2. What photos are needed

To be **ready**: **5 sharp close-ups (`face`)** and **2 full-length (`full`)**; a waist-up (`half`) is optional. Up to 8 per `create_face_profile` call. `get_face_profile` also reports the advised counts (about 10 close-ups, 6 full-length, 4 waist-up give the best likeness) and the limits (20, 12 and 10 photos per kind): offer to add more only when the likeness is weak.

Good photos: one person, one face, sharp, evenly lit, face large in the frame, no sunglasses, no heavy filters or beauty modes, mouth and eyes visible. Vary angle and expression a little (straight, slight turn left and right, a smile, a calm face); keep the hairstyle and any beard the way the user wants to be drawn. Full-length: head to shoes, plain background, normal fitted clothes so the real build is visible: the model copies the body it sees, so do not suggest flattering angles.

The server checks every photo at once and keeps only the good ones; a bad one comes back with reasons. Pass the reasons on and ask for a replacement.

## 3. Add the photos

Both ways work, a local file does **not** need a public link:
- Files on the user's machine: send them as `image_base64` (one photo per `add_face_photo`, under 25 MB; or up to 8 in `create_face_profile` within 16 MB in total).
- Public links: `url`.

Order: the user's confirmation first, then `face_profile_consent` (or `create_face_profile` which takes consent and photos together), then the photos, then `get_face_profile` to confirm it is ready. Remove a bad photo with `delete_face_photo` (ids come from `get_face_profile`).

## 4. Use it

- **A character of the user:** `make_character` with `use_face_profile: true` and a `style` from `list_character_styles` (97 styles, names in kk/ru/en; there is a "same person, new clothes" style and a video character sheet style). Say what they wear in `note`; `pose` takes a pose id or a short phrase; `count` up to 4. It is free, like all images.
- **Their face in any other picture** (a thumbnail, a poster, an ad): `generate_image` cannot read the profile directly, so first make one or two good pictures of them with `make_character` (`use_face_profile: true`), then pass those result URLs as `reference_image_urls` to the next generation with the sentence "the person from image 1, exactly the same face, do not beautify, average or restyle it". Check the result against the real photos (the server scores likeness for profile shoots; for your own generations compare by eye and say so).
- **Video:** Seedance refuses photos of real people. A real face in a video needs the account's registered likeness asset; otherwise make the character an illustration, or keep the real person out of the clip. Kling accepts real faces for edits.

## 5. When the likeness is poor

Cause and fix: the template or reference picture contains another person and the model copies that face (put the user's face pictures first and the template last); the reference photos disagree (remove the odd one); too many references crowd the face (fewer, sharper). The profile photo mix is also the bar: very similar photos set a high bar for "same person".

## 6. Deliver

Say what is now in the profile (counts, ready or not), give the picture URLs, and remind the user that they can delete the profile at any time. Do not repeat IDs or paste photo data into the chat.
