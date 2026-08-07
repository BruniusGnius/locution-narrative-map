#!/usr/bin/env python3
import json
import os
from pathlib import Path


def _flatten_mlx_words(result: dict) -> list[dict]:
    words = []
    for seg in result.get("segments", []):
        for item in seg.get("words", []) or []:
            if "start" in item and "end" in item:
                words.append({
                    "word": str(item.get("word", "")).strip(),
                    "start": round(float(item["start"]), 3),
                    "end": round(float(item["end"]), 3),
                    "probability": item.get("probability"),
                })
    return words


def transcribe_mlx(audio: Path, model: str, language: str | None) -> dict:
    import mlx_whisper
    kwargs = {
        "path_or_hf_repo": model,
        "word_timestamps": True,
        "temperature": 0,
    }
    if language and language != "auto":
        kwargs["language"] = language
    result = mlx_whisper.transcribe(str(audio), **kwargs)
    return {
        "backend": "mlx",
        "model": model,
        "language": result.get("language", language),
        "text": result.get("text", "").strip(),
        "segments": result.get("segments", []),
        "words": _flatten_mlx_words(result),
    }


def transcribe_faster(audio: Path, model: str, language: str | None) -> dict:
    from faster_whisper import WhisperModel
    wm = WhisperModel(model, device="cpu", compute_type="int8")
    kwargs = {"beam_size": 5, "word_timestamps": True, "vad_filter": True}
    if language and language != "auto":
        kwargs["language"] = language
    segments_iter, info = wm.transcribe(str(audio), **kwargs)
    segments = []
    words = []
    texts = []
    for s in segments_iter:
        text = s.text.strip()
        texts.append(text)
        seg_words = []
        for w in s.words or []:
            item = {
                "word": w.word.strip(),
                "start": round(float(w.start), 3),
                "end": round(float(w.end), 3),
                "probability": getattr(w, "probability", None),
            }
            words.append(item)
            seg_words.append(item)
        segments.append({"start": float(s.start), "end": float(s.end), "text": text, "words": seg_words})
    return {
        "backend": "faster-whisper",
        "model": model,
        "language": getattr(info, "language", language),
        "language_probability": getattr(info, "language_probability", None),
        "text": " ".join(t for t in texts if t).strip(),
        "segments": segments,
        "words": words,
    }


def transcribe(audio: Path, manifest: dict, profile: str, language: str | None) -> dict:
    backend = manifest["backend"]
    model = manifest["models"][backend][profile]
    ffmpeg = Path(manifest["ffmpeg"])
    runtime_home = Path(manifest["home"])
    cache_home = runtime_home / "cache"
    os.environ["PATH"] = str(ffmpeg.parent) + os.pathsep + os.environ.get("PATH", "")
    os.environ.setdefault("IMAGEIO_FFMPEG_EXE", str(ffmpeg))
    os.environ.setdefault("HF_HOME", str(cache_home / "huggingface"))
    os.environ.setdefault("XDG_CACHE_HOME", str(cache_home / "xdg"))
    if backend == "mlx":
        return transcribe_mlx(audio, model, language)
    return transcribe_faster(audio, model, language)


def to_srt(words: list[dict], max_words: int = 9, max_seconds: float = 4.5) -> str:
    def tc(s: float) -> str:
        ms = int(round(s * 1000))
        h, rem = divmod(ms, 3600000)
        m, rem = divmod(rem, 60000)
        sec, milli = divmod(rem, 1000)
        return f"{h:02d}:{m:02d}:{sec:02d},{milli:03d}"
    groups, current = [], []
    for w in words:
        if current and (len(current) >= max_words or w["end"] - current[0]["start"] > max_seconds):
            groups.append(current)
            current = []
        current.append(w)
    if current:
        groups.append(current)
    out = []
    for i, g in enumerate(groups, 1):
        out += [str(i), f"{tc(g[0]['start'])} --> {tc(g[-1]['end'])}", " ".join(x["word"] for x in g).strip(), ""]
    return "\n".join(out)
