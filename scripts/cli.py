#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from audio_probe import probe
from diarize import safe_diarize
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


def build_context(args) -> dict:
    context = {}
    if args.context_file:
        context = json.loads(Path(args.context_file).expanduser().read_text(encoding="utf-8"))
    if args.topic:
        context["general_topic"] = args.topic
    if args.content_type:
        context["content_type"] = args.content_type
    if args.language and args.language != "auto":
        context["primary_language"] = args.language
    if args.secondary_language:
        context["secondary_languages"] = args.secondary_language
    if args.glossary_term:
        context["glossary"] = args.glossary_term
    if args.speakers:
        context["expected_speakers"] = args.speakers
    context.setdefault("preserve_foreign_terms", True)
    return context


def speaker_for_range(start: float, end: float, segments: list[dict]) -> tuple[str | None, str | None]:
    best = None
    best_overlap = 0.0
    for seg in segments:
        overlap = max(0.0, min(end, float(seg["end"])) - max(start, float(seg["start"])))
        if overlap > best_overlap:
            best_overlap = overlap
            best = seg
    if best is None:
        return None, None
    return best.get("speaker_id"), best.get("speaker_label")


def build_phrase_map(acoustic_phrases: list[dict], words: list[dict], speaker_segments: list[dict] | None = None) -> list[dict]:
    """Attach transcript text and, when available, speaker labels to acoustic phrases."""
    speaker_segments = speaker_segments or []
    mapped = []
    for phrase in acoustic_phrases:
        start = float(phrase["start"])
        end = float(phrase["end"])
        phrase_words = []
        for w in words:
            ws = float(w.get("start", 0.0))
            we = float(w.get("end", ws))
            midpoint = (ws + we) / 2.0
            if start <= midpoint <= end:
                phrase_words.append(w)
        speaker_id, speaker_label = speaker_for_range(start, end, speaker_segments)
        item = dict(phrase)
        item["text"] = " ".join(w.get("word", "").strip() for w in phrase_words if w.get("word", "").strip()).strip()
        item["word_count"] = len(phrase_words)
        item["speaker_id"] = speaker_id
        item["speaker_label"] = speaker_label
        mapped.append(item)
    return mapped


def cmd_prepare(home: Path, audio: Path, output: Path, profile: str, language: str, context: dict, diarization_mode: str) -> int:
    manifest = load_manifest(home)
    output.mkdir(parents=True, exist_ok=True)
    ffmpeg = Path(manifest["ffmpeg"])

    probe_data = probe(audio, ffmpeg)
    (output / "acoustic-map.json").write_text(json.dumps(probe_data, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "context.json").write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

    tx = transcribe(audio, manifest, profile, language, context)
    (output / "transcript.json").write_text(json.dumps(tx, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "words.json").write_text(json.dumps(tx["words"], ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "transcript.txt").write_text(tx["text"] + "\n", encoding="utf-8")
    (output / "transcript.srt").write_text(to_srt(tx["words"]), encoding="utf-8")

    expected_speakers = context.get("expected_speakers")
    if diarization_mode == "off":
        speaker_map = {
            "status": "disabled",
            "count": expected_speakers if expected_speakers else None,
            "count_source": "user_hint" if expected_speakers else "unknown",
            "expected_speakers": expected_speakers,
            "speakers": [],
            "segments": [],
        }
    else:
        speaker_map = safe_diarize(audio, manifest, expected_speakers)
    (output / "speaker-map.json").write_text(json.dumps(speaker_map, ensure_ascii=False, indent=2), encoding="utf-8")

    phrase_map = build_phrase_map(probe_data["acoustic_phrases"], tx["words"], speaker_map.get("segments", []))
    (output / "phrase-map.json").write_text(json.dumps(phrase_map, ensure_ascii=False, indent=2), encoding="utf-8")

    handoff = {
        "source": str(audio.resolve()),
        "duration": probe_data["duration"],
        "context": context,
        "transcription": {
            "backend": tx["backend"],
            "model": tx["model"],
            "language": tx.get("language"),
            "text": tx["text"],
            "words": tx["words"],
            "initial_prompt_used": tx.get("initial_prompt_used"),
        },
        "speakers": speaker_map,
        "acoustic_phrases": phrase_map,
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
    p.add_argument("--topic")
    p.add_argument("--content-type")
    p.add_argument("--secondary-language", action="append", default=[])
    p.add_argument("--glossary-term", action="append", default=[])
    p.add_argument("--speakers", type=int)
    p.add_argument("--context-file")
    p.add_argument("--diarization", choices=["auto", "off"], default="auto")

    args = ap.parse_args()
    home = Path(args.home).expanduser().resolve()
    if args.command == "doctor":
        return cmd_doctor(home, args.json)
    if args.command == "prepare":
        context = build_context(args)
        return cmd_prepare(
            home,
            Path(args.audio).expanduser().resolve(),
            Path(args.output).expanduser().resolve(),
            args.profile,
            args.language,
            context,
            args.diarization,
        )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
