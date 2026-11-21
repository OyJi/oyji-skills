#!/usr/bin/env python3
"""Word-exact timings for a narration take, from a local speech-to-text model (nothing leaves the machine).

The script you wrote is the truth for the WORDS; the audio only supplies the TIMES. Whisper's own spelling of
Kazakh is not trusted: its words are matched to the script words, and script words it missed get times
interpolated between their matched neighbours.

    ~/.oyji-skills-venv/bin/python word_timing.py voice01.mp3 --text "the exact line" --lang kk --out words01.json

Options:
  --model  a faster-whisper model name or a local folder. Default: the first folder found at
           ~/.cache/huggingface/hub/models--Systran--faster-whisper-*/snapshots/*  (medium is already there),
           else the name "medium" (which would download it: pass --offline to refuse).
  --offline  never download a model.

Output: {"audio": ..., "duration": 6.19, "words": [{"word": "Көк", "start": 0.24, "end": 0.51, "matched": true}, ...],
         "matched_ratio": 0.92}
Use the JSON as a block's "words" in assemble.py. Run once per take. Needs `pip install faster-whisper`
in its own venv (see ../../README.md); the model weights are not downloaded by this script unless you omit --offline.
"""
import argparse
import difflib
import glob
import json
import os
import re
import sys


def norm(w):
    return re.sub(r"[^\w]", "", w.lower().replace("ё", "е"))


def default_model():
    hits = sorted(glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--Systran--faster-whisper-*/snapshots/*")))
    hits = [h for h in hits if os.path.exists(os.path.join(h, "model.bin"))]
    medium = [h for h in hits if "medium" in h]
    return (medium or hits or [None])[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--text", required=True, help="the exact script line spoken in this take")
    ap.add_argument("--lang", default="kk")
    ap.add_argument("--model")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster_whisper is not installed in this Python. Use the venv described in the README.")

    model_ref = a.model or default_model()
    if not model_ref:
        if a.offline:
            sys.exit("No local faster-whisper model found and --offline was given.")
        model_ref = "medium"
    model = WhisperModel(model_ref, device="cpu", compute_type="int8", local_files_only=a.offline or os.path.isdir(model_ref or ""))
    # the script as a prompt steers the spelling and the names toward what was meant to be said
    segs, info = model.transcribe(a.audio, language=a.lang, word_timestamps=True, vad_filter=False, beam_size=5,
                                  initial_prompt=a.text, condition_on_previous_text=False)
    heard = []
    for s in segs:
        for w in (s.words or []):
            heard.append({"word": w.word.strip(), "start": float(w.start), "end": float(w.end)})
    dur = float(info.duration)

    script = a.text.split()
    S = [norm(w) for w in script]
    H = [norm(w["word"]) for w in heard]
    sm = difflib.SequenceMatcher(a=S, b=H, autojunk=False)
    times = [None] * len(script)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            h = heard[blk.b + k]
            times[blk.a + k] = (h["start"], h["end"])

    # fuzzy rescue for words that differ by a letter or two (Kazakh endings are often misspelled by the model)
    used = {id(t) for t in times if t}
    for i, w in enumerate(S):
        if times[i] is None and heard:
            lo = max((times[j][1] for j in range(i) if times[j]), default=0.0)
            hi = min((times[j][0] for j in range(i + 1, len(S)) if times[j]), default=dur)
            best, score = None, 0.0
            for hw, hn in zip(heard, H):
                if hw["start"] >= lo - 0.05 and hw["end"] <= hi + 0.05:
                    r = difflib.SequenceMatcher(a=w, b=hn).ratio()
                    if r > score:
                        best, score = hw, r
            if best and score >= 0.6:
                times[i] = (best["start"], best["end"])

    matched = sum(1 for t in times if t)
    # interpolate the rest between known neighbours, weighted by word length
    start0 = heard[0]["start"] if heard else 0.0
    end0 = heard[-1]["end"] if heard else dur
    i = 0
    while i < len(script):
        if times[i]:
            i += 1
            continue
        j = i
        while j < len(script) and not times[j]:
            j += 1
        lo = times[i - 1][1] if i > 0 else start0
        hi = times[j][0] if j < len(script) else end0
        weights = [max(len(S[k]), 1) for k in range(i, j)]
        tot = sum(weights)
        t = lo
        for k, wgt in zip(range(i, j), weights):
            seg = (hi - lo) * wgt / tot
            times[k] = (t, t + seg)
            t += seg
        i = j

    words = []
    for w, t, n in zip(script, times, S):
        words.append({"word": w, "start": round(t[0], 3), "end": round(t[1], 3)})
    for k, w in enumerate(words):
        w["matched"] = k < len(script) and any(abs(w["start"] - h["start"]) < 1e-3 for h in heard)
    out = {"audio": os.path.basename(a.audio), "duration": round(dur, 3), "words": words,
           "matched_ratio": round(matched / max(len(script), 1), 3), "heard": " ".join(h["word"] for h in heard)}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved %s: %d words, %d%% matched to what was heard" % (a.out, len(words), round(100 * out["matched_ratio"])))


if __name__ == "__main__":
    main()
