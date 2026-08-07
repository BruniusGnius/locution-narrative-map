#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path

DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)")
SILENCE_START_RE = re.compile(r"silence_start:\s*([0-9.]+)")
SILENCE_END_RE = re.compile(r"silence_end:\s*([0-9.]+)")


def probe(audio: Path, ffmpeg: Path, noise: str = "-40dB", min_silence: float = 0.25) -> dict:
    cmd = [
        str(ffmpeg), "-hide_banner", "-i", str(audio),
        "-af", f"silencedetect=noise={noise}:d={min_silence}",
        "-f", "null", "-",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    stderr = p.stderr
    m = DURATION_RE.search(stderr)
    if not m:
        raise RuntimeError("Could not determine media duration")
    h, mnt, sec = int(m.group(1)), int(m.group(2)), float(m.group(3))
    duration = h * 3600 + mnt * 60 + sec

    starts = [float(x) for x in SILENCE_START_RE.findall(stderr)]
    ends = [float(x) for x in SILENCE_END_RE.findall(stderr)]
    silences = []
    end_i = 0
    for start in starts:
        while end_i < len(ends) and ends[end_i] < start:
            end_i += 1
        end = ends[end_i] if end_i < len(ends) else duration
        silences.append({"start": round(start, 3), "end": round(min(end, duration), 3)})
        end_i += 1

    speech = []
    cursor = 0.0
    for s in silences:
        if s["start"] > cursor:
            speech.append([cursor, s["start"]])
        cursor = max(cursor, s["end"])
    if cursor < duration:
        speech.append([cursor, duration])

    # Merge tiny speech fragments into a neighbor to avoid promoting breaths/interjections to phrases.
    merged = []
    for start, end in speech:
        if merged and end - start < 1.2:
            merged[-1][1] = end
        else:
            merged.append([start, end])
    phrases = [
        {"phrase_id": f"P{i:02d}", "start": round(a, 3), "end": round(b, 3), "duration": round(b-a, 3)}
        for i, (a, b) in enumerate(merged, 1) if b - a > 0.05
    ]
    return {
        "duration": round(duration, 3),
        "silence_threshold": noise,
        "minimum_silence": min_silence,
        "silences": silences,
        "acoustic_phrases": phrases,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--ffmpeg", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    result = probe(Path(args.audio), Path(args.ffmpeg))
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
