---
name: oyji-creature
description: Make photoreal creatures, hybrids, mythic beings and costumed characters through the OyJI MCP (image generation is free). Builds the picture in stages - grey clay shape, a real face or animal donor, close-up material swatches, then one deliberately plain flash photo - so the result looks photographed, not rendered, and survives animation later. Use when the user asks for a creature, monster, spirit, alien, hybrid or character (Kazakh folklore included) that must look like a real subject on a film set.
---

# OyJI Creature

Goal: the creature reads as **a real living thing photographed on a set**. Not a render, not a figurine, not concept art.

Needs the OyJI MCP connected (`generate_image`, `upload_from_url`, `list_media`, `get_media`). Images cost nothing; videos cost money, so never start one without the user's clear yes (see `oyji-video-director`).

## Tool facts (verified on the OyJI server)

- Image model: `nano-banana-pro`. Up to **6 reference images** per call, up to 4 results per call, ratios 1:1, 3:4, 4:3, 9:16, 16:9.
- A URL returned by an earlier generation can go straight into `reference_image_urls`. A file on the user's disk cannot: it must first be a public URL, then `upload_from_url`.
- `strict: true` tells the model to change only what the prompt names. Use it for small fixes, not for the skin pass.
- Six references means: 1 clay + 1 donor + **at most 4 material swatches**. Plan the materials around that limit.

## Run it without asking permission between steps

1. Design the character.
2. Pick the track.
3. Clay (3 takes, choose one).
4. Donor photo.
5. Swatches.
6. Skin pass (2 takes).
7. Look at the result, run the check, fix one block, run once more.

Show each result as it arrives. Keep every image URL: later steps use them as references, so the user uploads nothing.

## 1. Design (one sentence from the user is enough; fill the gaps yourself)

- **Role**: what it does in its world (judge, shepherd, tax collector, smith, pilgrim). A role gives props and a pose.
- **Donor species**: two or three exact animals. Not "a bird" but "a steppe eagle"; not "a lizard" but "a thorny devil". First donor = head, second = covering or weapon, third = one detail.
- **How the hybrid is joined** (pick one): a replaced part, a body that is a home, growth out of the body, the lower half of another animal, a whole animal in a human role, an object that became an organ, a moult, a symbiont.
- **One trace of its past**: a scar, a trophy, a repair, a debt.
- **A pose with presence**: still and superior. Never a T-pose.
- **Palette from nature**: one dominant, one secondary, **one** bright accent, colours taken from the real species.
- **Scale**: height in metres plus one everyday object to compare with.

Quality rules: the silhouette reads in three seconds; one big mass, two or three medium, many small; every part has a function; about 70% real anatomy and 30% strange; dignity, not disgust; one focal point.

Kazakh seeds when the user has no idea: donors - grey wolf, steppe eagle, Bactrian camel, saiga, goitered gazelle, kulan, wild horse, argali, snake, owl. Materials - pressed felt (kiiz), cured hide, horse leather, ram horn, silver filigree, bronze, rusty iron mail, raw silk, wool, bone. Figures - Kok Bori, Zhalmauyz Kempir, Albasty, Samruk, winged Tulpar, Aidahar, Zhezkiik. Original designs only; never copy a known franchise character.

## 2. Pick the track

| Track | Who | Stages |
|---|---|---|
| A. Humanlike (human face or skin) | half-human, an old man with animal parts, an elf | clay, human donor, skin pass |
| B. Creature (no human skin) | animal character, object-creature, alien, fish, fungus | clay, animal donor (optional), skin pass |
| C. Woman or fairy in a costume of natural material | shell, feather, wing costumes | clay, human donor, skin pass |

Three rules on every track:
1. Put at least one real-material swatch into every skin pass.
2. A human face or skin always comes from a separate donor photo, never from the clay alone.
3. The stranger the creature, the plainer the photo.

## 3. Clay

Prompt skeleton (write the capitalised name in the middle, keep the rest):

```
Digital sculpture render of a <NAME>: <who it is and the pose>, <face; for track A say "clearly visible human face">, <how the hybrid is joined, in detail>, <two or three props of its role>. Waist-up bust, front view facing the camera, figure fills the frame. Whole figure one unpainted matte grey clay material, no color, extreme sculpted detail, single figure, one view, no base, no text, soft key light and rim light, pure black background
```

- Ratio 16:9 for a bust when the face is the hook; 3:4 for a full figure or a costume; 4:3 for a long four-legged animal. Use the same ratio in the skin pass.
- Make 3 takes. Name no colours. "single figure, one view" is required, or the model draws a turnaround of two.
- Check: silhouette reads, face visible, one grey material, the hybrid joint is visible. If not, rewrite the description; do not rerun the same prompt.

## 4. Donor photo

- Animal face: `Wildlife photograph of a real <species>, head and neck close-up, looking straight into the camera, natural light, real fur detail, sharp focus, no text`. Ratio 4:3.
- Human face: a plain flash portrait of an invented adult, against a dark wall, real skin texture and pores. Match the clay in age and mood. Adults only, and never the face of a real named person. If the user wants their own face, use the OyJI face-profile tools and only after they confirm the photos are of themselves.
- Look at it before using it. A crooked nose or extra teeth means another take.

## 5. Swatches

One extreme close-up of one real material, 1:1:

```
extreme macro photograph of real <material> filling the whole frame edge to edge, <colour, texture, wear>, hard direct flash, sharp focus, real texture, no text
```

Make one per important material and reuse it across creatures in the same chat. Name the material by its species or exact kind ("old rusty riveted chain mail", not "armor"). Invented materials stand on a real one plus one shift (the colour of another species, a different scale, an infestation). Never glow, neon, crystals or "magic energy".

## 6. Skin pass

References, in order: **image 1 clay, image 2 donor, images 3+ swatches (max 6 in total)**. The prompt gives every picture one job:

```
Image 1 is the base: keep pose, proportions, composition and every sculpted feature exactly (list them). Turn this grey sculpture into a real photo of <who it is>.
<Head/face> is exactly the real <animal/person> from image 2; fur or skin grows naturally out of it, no seams.
<Part> is the real <material> from image N: <colour, texture, wear>.
<Other parts>: real <exact material>, <colour>, <wear>.
<The one bright accent> is the only bright colour; everything else keeps the natural colours of the real materials.
<photo block>
```

Rules: name every sculpted feature so nothing drifts; map every material to a body part and a picture; write in the parts the clay never had (armour, trophies); give each part colour, texture and wear. Do the skin pass once per character: repeats lower the face.

Photo block, pick one (change only this block when you change the mode):
- **Makeup test**: direct frontal flash, dark grey seamless paper behind, hard clear shadow on the paper, shallow depth of field, no shine, no clay or CG look.
- **Phone snapshot** (default for maximum realism): casual phone flash in a dim room, subject close against a dark charcoal wall, hard frontal flash, sharp shadow on the wall, slight noise, unsaturated colours, "not cinematic", life-size with stray hairs and dust, no sculpture or toy look, do not change pose or composition.

Soft light on a black background makes a render. Giants: state the height and put an everyday object in frame for scale.

## 7. Check before showing (look at the images, do not assume)

1. Photo or render? Flash straight on, dark wall close behind, a sharp shadow.
2. Face real (pores, asymmetry) and matches the donor.
3. Three texture families can be told apart: hard, soft, wet.
4. One bright accent only.
5. Pose and composition did not drift from the clay.
6. Nothing glows; the costume covers the body.
7. It reads life-size, not like a figurine on a table.
8. You can say what it works with, what has happened to it, and whose it is.
9. At least one swatch visibly shaped the result.

If it fails, rewrite one block and run once more.

## Known limits (pilot, 2026-11-20)

- A small part (a collar of mail) can lose its swatch in the final. Repeat that material by name and size in the prompt, or fix it in a separate pass with `strict: true`.
- A one-line prompt on `nano-banana-pro` is already good. The staged recipe gives tactile texture, a believable face and control; do not promise a miracle. Its real value shows when the picture is animated.
- Text on small objects morphs in video. Keep the creature free of readable text.

## Then animate

Use `oyji-video-director` with the finished photo (and a location from `oyji-location`).
