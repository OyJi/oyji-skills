#!/usr/bin/env python3
"""Put a presenter (a talking-head clip) in a corner of a finished video, round or rounded, with their audio or the
video's own. The presenter clip comes from the user (their own recording) or from `oyji-video-director`
(a generated talking character); this script only composites. Needs ffmpeg, ffprobe and Pillow.

    python3 -I presenter_overlay.py --base final.mp4 --presenter talk.mp4 --out final_presenter.mp4
        [--position bottom-left|bottom-right|top-left|top-right]   default bottom-right
        [--size 0.30]            presenter width as a fraction of the video width
        [--shape circle|rounded|square]                              default circle
        [--audio base|presenter|mix]                                 default presenter (base audio dropped); mix keeps both
        [--margin 0.04]          distance from the edges, fraction of the video width
        [--start 0] [--end SECONDS]   when the presenter is on screen (default: the presenter clip's own length)
        [--ring "#FFFFFF"]       optional thin ring colour around the presenter

Never put a presenter on the video unless the user asked for one; never infer it from a photo that happens to be around.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd) + "\n" + r.stderr[-1500:])
    return r.stdout


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-show_entries",
               "format=duration", "-of", "json", path])
    j = json.loads(out)
    return int(j["streams"][0]["width"]), int(j["streams"][0]["height"]), float(j["format"]["duration"])


def has_audio(path):
    return bool(run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", path]).strip())


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def make_mask(size, shape, ring):
    S = size * 4  # supersample for smooth edges
    mask = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(mask)
    if shape == "circle":
        d.ellipse((0, 0, S - 1, S - 1), fill=255)
    elif shape == "rounded":
        d.rounded_rectangle((0, 0, S - 1, S - 1), radius=S // 6, fill=255)
    else:
        d.rectangle((0, 0, S - 1, S - 1), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    ring_img = None
    if ring:
        rw = max(2, size // 40)
        big = Image.new("L", (S, S), 0)
        bd = ImageDraw.Draw(big)
        if shape == "circle":
            bd.ellipse((0, 0, S - 1, S - 1), outline=255, width=rw * 4)
        elif shape == "rounded":
            bd.rounded_rectangle((0, 0, S - 1, S - 1), radius=S // 6, outline=255, width=rw * 4)
        else:
            bd.rectangle((0, 0, S - 1, S - 1), outline=255, width=rw * 4)
        ring_img = big.resize((size, size), Image.LANCZOS)
    return mask, ring_img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--presenter", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--position", default="bottom-right", choices=["bottom-left", "bottom-right", "top-left", "top-right"])
    ap.add_argument("--size", type=float, default=0.30)
    ap.add_argument("--shape", default="circle", choices=["circle", "rounded", "square"])
    ap.add_argument("--audio", default="presenter", choices=["base", "presenter", "mix"])
    ap.add_argument("--margin", type=float, default=0.04)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--ring")
    a = ap.parse_args()

    W, H, bd = probe(a.base)
    pw, ph, pd = probe(a.presenter)
    S = int(round(W * a.size / 2)) * 2
    m = int(W * a.margin)
    x = m if "left" in a.position else W - S - m
    y = m if "top" in a.position else H - S - m
    if a.position.startswith("bottom"):
        y = min(y, int(H * 0.78) - S)  # stay above the caption band that assemble.py burns into the lower fifth
    end = a.end if a.end is not None else min(bd, a.start + pd)

    tmp = tempfile.mkdtemp(prefix="oyji-presenter-")
    mask, ring_img = make_mask(S, a.shape, a.ring)
    mpath = os.path.join(tmp, "mask.png")
    mask.save(mpath)
    inputs = ["-i", a.base, "-i", a.presenter, "-loop", "1", "-framerate", "24", "-i", mpath]
    ring_in = ""
    if ring_img is not None:
        rimg = Image.new("RGBA", (S, S), hex_rgb(a.ring) + (0,))
        rimg.putalpha(ring_img)
        rpath = os.path.join(tmp, "ring.png")
        rimg.save(rpath)
        inputs += ["-loop", "1", "-framerate", "24", "-i", rpath]
        ring_in = "[3:v]format=rgba[ring];"

    fc = ("[1:v]setpts=PTS-STARTPTS+%.3f/TB,scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,format=rgba[p];"
          "[2:v]format=gray,scale=%d:%d[m];[p][m]alphamerge[pm];%s"
          "[0:v][pm]overlay=%d:%d:eof_action=pass:enable='between(t,%.3f,%.3f)'") % (a.start, S, S, S, S, S, S, ring_in, x, y, a.start, end)
    if ring_in:
        fc += "[tmp];[tmp][ring]overlay=%d:%d:shortest=1:enable='between(t,%.3f,%.3f)'" % (x, y, a.start, end)
    fc += "[v]"

    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc]
    maps = ["-map", "[v]"]
    p_audio = has_audio(a.presenter)
    b_audio = has_audio(a.base)
    delay_ms = int(a.start * 1000)
    if a.audio == "presenter" and p_audio:
        cmd = cmd[:-2] + ["-filter_complex", fc + ";[1:a]adelay=%d|%d[pa]" % (delay_ms, delay_ms)]
        maps += ["-map", "[pa]"]
    elif a.audio == "mix" and p_audio and b_audio:
        cmd = cmd[:-2] + ["-filter_complex", fc + ";[1:a]adelay=%d|%d[pa];[0:a][pa]amix=inputs=2:duration=first:dropout_transition=0[a]" % (delay_ms, delay_ms)]
        maps += ["-map", "[a]"]
    elif b_audio:
        maps += ["-map", "0:a"]
    cmd += maps + ["-t", "%.3f" % bd, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                   "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out]
    run(cmd)
    print("saved %s  %dx%d  presenter %dpx %s at %s, on screen %.1f-%.1f s, audio: %s" % (a.out, W, H, S, a.shape, a.position, a.start, end, a.audio))


if __name__ == "__main__":
    main()
