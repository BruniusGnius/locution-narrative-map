#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

from audio_probe import probe
from doctor import run_doctor
from transcribe import to_srt, transcribe


def load_manifest(home: Path) -> dict:
    p = home / "runtime.json"
    if not p.exists():
        raise RuntimeError("Runtime manifest missing. Run bootstrap first.")
    return json.loads(p.read_text(encoding="utf-8"))


def cmd_doctor(home: Path, as_json: bool) -> int:
    report = run_doctor(home)
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        for k, v in report["checks"].items():
            print(f"{k}: {v}")
        print(f"backend: {report.get('backend', 'unknown')}")
        print("OK" if report["ok"] else "NEEDS_REPAIR")
    return 0 if report["ok"] else 1


def cmd_prepare(home: Path, audio: Path, output: Path, profile: str, language: str) -> int:
    manifest = load_manifest(home)
    output.mkdir(parents=True, exist_ok=True)
    ffmpeg = Path(manifest["ffmpeg"])

    probe_data = probe(audio, ffmpeg)
    (output / "acoustic-map.json").write_text(json.dumps(probe_data, ensure_ascii=False, indent=2), encoding="utf-8")

    tx = transcribe(audio, manifest, profile, language)
    (output / "transcript.json").write_text(json.dumps(tx, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "words.json").write_text(json.dumps(tx["words"], ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "transcript.txt").write_text(tx["text"] + "\n", encoding="utf-8")
    (output / "transcript.srt").write_text(to_srt(tx["words"]), encoding="utf-8")

    handoff = {
        "source": str(audio.resolve()),
        "duration": probe_data["duration"],
        "transcription": {
            "backend": tx["backend"],
            "model": tx["model"],
            "language": tx.get("language"),
            "text": tx["text"],
            "words": tx["words"],
        },
        "acoustic_phrases": probe_data["acoustic_phrases"],
        "semantic_beats": [],
        "note": "semantic_beats must be created by the agent from textual evidence; acoustic phrases are not narrative beats",
    }
    (output / "handoff.json").write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(output / "handoff.json"))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="locution-narrative-map")
    ap.add_argument("--home", required=True)
    sub = ap.add_subparsers(dest="command", required=True)

    d = sub.add_parser("doctor")
    d.add_argument("--json", action="store_true")

    p = sub.add_parser("prepare")
    p.add_argument("audio")
    p.add_argument("--output", required=True)
    p.add_argument("--profile", choices=["fast", "balanced", "quality"], default="balanced")
    p.add_argument("--language", default="auto")

    args = ap.parse_args()
    home = Path(args.home).expanduser().resolve()
    if args.command == "doctor":
        return cmd_doctor(home, args.json)
    if args.command == "prepare":
        return cmd_prepare(home, Path(args.audio).expanduser().resolve(), Path(args.output).expanduser().resolve(), args.profile, args.language)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
