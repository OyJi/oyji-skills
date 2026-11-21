#!/usr/bin/env python3
"""Assemble a narrated picture video: one image + one narration take per block, Ken Burns motion,
optional music bed and burned-in captions. Needs ffmpeg and ffprobe. Narration is never sped up:
each block lasts exactly as long as its audio (plus a short tail), and the script refuses a take
that is far shorter or longer than the window you planned.

    python3 assemble.py manifest.json

manifest.json:
{
  "out": "final.mp4",
  "aspect": "9:16",                  # "9:16" | "16:9" | "1:1"
  "fps": 24,
  "tail": 0.35,                      # seconds of picture after each spoken line
  "window": 10,                      # planned seconds per block (for the timing gate); null to skip
  "tolerance": 0.35,                 # allowed relative difference between take and window
  "motion": "kenburns",              # "kenburns" | "none"
  "blocks": [
    {"image": "frame01.png", "audio": "voice01.mp3", "caption": "Exact words of the line",
     "words": "words01.json"},       # optional: word-exact timing from word_timing.py (otherwise timed by characters)
    {"video": "clip02.mp4",  "audio": "voice02.mp3", "caption": "..."}   # a generated clip instead of a still
  ],
  "music": "bed.mp3",                # optional, ducked under the voice
  "music_volume": 0.12,
  "captions": true,                  # burn captions made from each block's "caption"
  "caption_font": "Arial",           # a font with Kazakh letters
  "caption_size": 3.2,               # text height, percent of the video height
  "caption_chars": 26                # max characters per caption line (default depends on the aspect)
}

Run with `python3 -I`. A clip given as "video" is trimmed or frozen on its last frame to fit the audio.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

SIZES = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080)}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd) + "\n" + r.stderr[-1500:])
    return r.stdout


def duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path])
    return float(out.strip())


def srt_time(t):
    ms = int(round(t * 1000))
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


def chunks(text, max_chars=34):
    words, out, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= max_chars or not cur:
            cur = t
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out or [""]


def main(spec):
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    W, H = SIZES[spec.get("aspect", "9:16")]
    fps = int(spec.get("fps", 24))
    tail = float(spec.get("tail", 0.35))
    window = spec.get("window")
    tol = float(spec.get("tolerance", 0.35))
    work = tempfile.mkdtemp(prefix="oyji-faceless-")
    parts, durs = [], []

    for i, b in enumerate(spec["blocks"], 1):
        a = P(b["audio"])
        ad = duration(a)
        if window and abs(ad - window) > window * tol:
            sys.exit("Block %d: the take is %.1f s but the window is %d s (allowed +-%d%%). Rewrite the line and regenerate it; do not speed it up."
                     % (i, ad, window, int(tol * 100)))
        d = ad + tail
        clip = os.path.join(work, "b%02d.mp4" % i)
        if b.get("video"):
            vf = "scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,fps=%d,tpad=stop_mode=clone:stop_duration=%.2f,format=yuv420p" % (W, H, W, H, fps, d)
            run(["ffmpeg", "-v", "error", "-y", "-i", P(b["video"]), "-i", a, "-t", "%.3f" % d, "-vf", vf,
                 "-map", "0:v", "-map", "1:a", "-af", "apad=pad_dur=%.3f" % tail, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", clip])
        else:
            frames = int(round(d * fps))
            if spec.get("motion", "kenburns") == "kenburns":
                zoom = "min(zoom+%.5f,1.14)" % (0.14 / max(frames, 1))
                direction = i % 2  # alternate push-in and drift so the cuts do not feel identical
                x = "iw/2-(iw/zoom/2)" if direction else "(iw-iw/zoom)*on/%d" % max(frames, 1)
                vf = ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
                      "zoompan=z='%s':x='%s':y='ih/2-(ih/zoom/2)':d=%d:s=%dx%d:fps=%d,format=yuv420p") % (W * 2, H * 2, W * 2, H * 2, zoom, x, frames, W, H, fps)
            else:
                vf = "scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,fps=%d,format=yuv420p" % (W, H, W, H, fps)
            run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(fps), "-i", P(b["image"]), "-i", a, "-t", "%.3f" % d,
                 "-vf", vf, "-af", "apad=pad_dur=%.3f" % tail, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", clip])
        parts.append(clip)
        durs.append(d)

    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join("file '%s'\n" % p for p in parts))
    joined = os.path.join(work, "joined.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])

    cur = joined
    if spec.get("music"):
        mixed = os.path.join(work, "mixed.mp4")
        vol = float(spec.get("music_volume", 0.12))
        run(["ffmpeg", "-v", "error", "-y", "-i", cur, "-stream_loop", "-1", "-i", P(spec["music"]),
             "-filter_complex", "[1:a]volume=%.3f[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2[a]" % vol,
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", mixed])
        cur = mixed

    if spec.get("captions"):
        srt = os.path.join(work, "captions.srt")
        t, n, lines = 0.0, 1, []
        maxc = int(spec.get("caption_chars", {"9:16": 26, "1:1": 34, "16:9": 48}[spec.get("aspect", "9:16")]))
        for b, d in zip(spec["blocks"], durs):
            if b.get("words"):
                # word-exact timing from word_timing.py: group words into lines, show each line from its first word to the next line
                words = json.load(open(P(b["words"]), encoding="utf-8"))["words"]
                group, glen = [], 0
                groups = []
                for w in words:
                    add = len(w["word"]) + (1 if group else 0)
                    if group and glen + add > maxc:
                        groups.append(group)
                        group, glen = [], 0
                        add = len(w["word"])
                    group.append(w)
                    glen += add
                if group:
                    groups.append(group)
                for gi, g in enumerate(groups):
                    start = t + g[0]["start"]
                    end = t + (groups[gi + 1][0]["start"] if gi + 1 < len(groups) else g[-1]["end"] + 0.25)
                    lines += [str(n), "%s --> %s" % (srt_time(start), srt_time(min(end, t + d))), " ".join(w["word"] for w in g), ""]
                    n += 1
            elif b.get("caption"):
                cs = chunks(b["caption"], maxc)
                total = sum(max(len(c), 1) for c in cs)
                spoken = d - tail
                tt = t
                for c in cs:
                    seg = spoken * max(len(c), 1) / total
                    lines += [str(n), "%s --> %s" % (srt_time(tt), srt_time(tt + seg)), c, ""]
                    n += 1
                    tt += seg
            t += d
        open(srt, "w", encoding="utf-8").write("\n".join(lines))
        # libass sizes text on a 288-line frame, whatever the real height: 3.2 means about 3.2% of the height
        size = max(6, int(round(288 * float(spec.get("caption_size", 3.2)) / 100)))
        style = "FontName=%s,Fontsize=%d,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,Alignment=2,MarginV=%d" % (
            spec.get("caption_font", "Arial"), size, int(288 * 0.14))
        esc = srt.replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
        captioned = os.path.join(work, "captioned.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-i", cur, "-vf", "subtitles='%s':force_style='%s'" % (esc, style),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "copy", captioned])
        cur = captioned

    out = P(spec.get("out", "final.mp4"))
    run(["ffmpeg", "-v", "error", "-y", "-i", cur, "-c", "copy", "-movflags", "+faststart", out])
    print("saved %s  %.1f s  %dx%d  blocks=%d" % (out, duration(out), W, H, len(parts)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(json.load(open(sys.argv[1], encoding="utf-8")))
