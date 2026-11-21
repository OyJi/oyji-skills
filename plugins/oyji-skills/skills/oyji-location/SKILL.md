---
name: oyji-location
description: Make empty rooms, interiors and outdoor locations through the OyJI MCP that look like real photographed places, ready to be the setting where a character or creature is filmed. One prompt, no clay, no references. Use when the user asks for a room, corridor, yurt interior, street, ruin, set or any empty place, or wants to put a character "in this place".
---

# OyJI Location

Goal: an **empty place that looks photographed**, to be used as the location reference in a video.

Needs the OyJI MCP (`generate_image`). Model `nano-banana-pro`, ratio 16:9 (or 9:16 for vertical video). Images are free.

## The rule for places

Characters and props are built from a grey clay shape first. **Places are the exception: skip the clay and use no references.** A place built from clay comes out too perfect: straight lines, everything centred, video-game geometry. In a video the place is most of the frame, so if it looks fake the whole clip looks fake.

You want the opposite of perfect: nothing lines up exactly, padding sags, dust sits in the floor, things look placed by hand.

## How to run it

1. Take the user's description. If it is one line, design the place first: its shape, one landmark, what is on the walls, what the light comes from.
2. Write one prompt in the seven blocks below, one paragraph each, in this order.
3. Generate 2 takes and choose by eye (download the images and look at them).
4. Run the check. If it fails, rewrite one block and run once more.
5. When the place goes into a video, say exactly what to take from it (last section).

## The seven blocks

1. **What it is, and its shape.** Start `A photorealistic live-action film still of an empty location:` then name the place and describe the geometry plainly: cross-section, floor, walls, ceiling, how many bays, what closes the far end.
2. **The landmark and the walls.** One thing the eye goes to (a door, a window, a stove, an altar), described part by part. Then what repeats along the walls and the materials with their wear: seams, stains, scuffs, a film of water.
3. **The camera.** Where it stands, at what height, which way it points. Where the landmark sits in the frame and how large it is. A slight tilt if the shot needs it. "Natural proportions."
4. **The light.** Only from fixtures that exist in the place. Which are on and which are off, the brightest part of the frame, small accent lights, exposure ("dim low-key, clear air"), reflections.
5. **The lens.** Its character, where the focus is, what falls out of focus, how detail fades toward the edges. "No added flare streaks, no uniform blur border."
6. **The colour.** The shadows, the main surfaces, the light, and one warm or bright accent.
7. **Empty.** "The <place> is unoccupied, the floor clear where someone will stand: no people, no figures behind windows, no human reflections, no readable lettering. One continuous image."

Describe what is there; do not pile up style words.

Kazakh place seeds: a yurt interior with felt walls and a carpet, a winter shelter (qystau) with a clay stove, an abandoned Soviet village club, a roadside shop in a village, a cliff gorge with a stone arch, a field of old standing stones, a night steppe road under a clear sky.

## Check the place

1. Photo of a place, or a render? Nothing lines up exactly; wear, dust and use are visible.
2. One clear landmark, and you can say where it sits in the frame.
3. The light comes from fixtures you can see or place.
4. Empty: no people, no figures, no readable text.
5. The floor is clear where the character will stand or move.

## Using the place in a video

Give the video model two images: the character photo and the location still. Then say what each is for:

- The whole place: `Use image 1 for the character. From image 2 take only the place.`
- One element: `From image 2 take only the door with the lamp above it. Isolate it from everything else in that image: no corridor, walls, floor, ceiling lights.` Then say how big and how far that element is in the new scene.
- What the character keeps and drops: `Do not take its wall, floor, flash lighting, hard shadow or pose.`

Continue with `oyji-video-director`.
