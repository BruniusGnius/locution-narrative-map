#!/usr/bin/env python3
"""Optional local speaker diarization using sherpa-onnx.

Models are downloaded on first use into LNM_HOME/models/diarization.
If diarization cannot run, callers should preserve the rest of the pipeline and
report speaker information as unavailable rather than guessing.
"""
from __future__ import annotations

import bz2
import io
import json
import subprocess
import tarfile
import urllib.request
from pathlib import Path

SEGMENTATION_URL = (
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/"
    "speaker-segmentation-models/sherpa-onnx-pyannote-segmentation-3-0.tar.bz2"
)
EMBEDDING_URL = (
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/"
    "speaker-recongition-models/3dspeaker_speech_eres2net_base_sv_zh-cn_3dspeaker_16k.onnx"
)


def _download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".part")
    with urllib.request.urlopen(url, timeout=120) as src, tmp.open("wb") as dst:
        while True:
            chunk = src.read(1024 * 1024)
            if not chunk:
                break
            dst.write(chunk)
    tmp.replace(target)


def ensure_models(home: Path) -> dict:
    model_dir = home / "models" / "diarization"
    seg_dir = model_dir / "sherpa-onnx-pyannote-segmentation-3-0"
    seg_model = seg_dir / "model.int8.onnx"
    emb_model = model_dir / "3dspeaker_speech_eres2net_base_sv_zh-cn_3dspeaker_16k.onnx"
    if not seg_model.exists():
        archive = model_dir / "segmentation.tar.bz2"
        _download(SEGMENTATION_URL, archive)
        with tarfile.open(archive, mode="r:bz2") as tf:
            tf.extractall(model_dir)
        archive.unlink(missing_ok=True)
    if not emb_model.exists():
        _download(EMBEDDING_URL, emb_model)
    return {"segmentation": str(seg_model), "embedding": str(emb_model)}


def _audio_f32_mono_16k(audio: Path, ffmpeg: Path):
    import numpy as np
    cmd = [
        str(ffmpeg), "-v", "error", "-i", str(audio),
        "-ac", "1", "-ar", "16000", "-f", "f32le", "pipe:1",
    ]
    p = subprocess.run(cmd, capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype="<f4").copy()


def diarize(audio: Path, manifest: dict, expected_speakers: int | None = None) -> dict:
    import sherpa_onnx

    home = Path(manifest["home"])
    models = ensure_models(home)
    num_clusters = int(expected_speakers) if expected_speakers and expected_speakers > 0 else -1
    config = sherpa_onnx.OfflineSpeakerDiarizationConfig(
        segmentation=sherpa_onnx.OfflineSpeakerSegmentationModelConfig(
            pyannote=sherpa_onnx.OfflineSpeakerSegmentationPyannoteModelConfig(
                model=models["segmentation"]
            ),
        ),
        embedding=sherpa_onnx.SpeakerEmbeddingExtractorConfig(
            model=models["embedding"]
        ),
        clustering=sherpa_onnx.FastClusteringConfig(
            num_clusters=num_clusters,
            threshold=0.9 if num_clusters == -1 else 0.5,
        ),
        min_duration_on=0.3,
        min_duration_off=0.5,
    )
    if not config.validate():
        raise RuntimeError("Speaker diarization models are unavailable or invalid")
    sd = sherpa_onnx.OfflineSpeakerDiarization(config)
    samples = _audio_f32_mono_16k(audio, Path(manifest["ffmpeg"]))
    result = sd.process(samples).sort_by_start_time()
    segments = [
        {
            "start": round(float(r.start), 3),
            "end": round(float(r.end), 3),
            "speaker_id": f"S{int(r.speaker) + 1:02d}",
            "speaker_label": f"Voz {int(r.speaker) + 1}",
        }
        for r in result
    ]
    speaker_ids = sorted({x["speaker_id"] for x in segments})
    return {
        "status": "detected",
        "count": len(speaker_ids),
        "count_source": "user_hint+diarization" if num_clusters > 0 else "diarization",
        "expected_speakers": expected_speakers,
        "speakers": [
            {"speaker_id": sid, "label": f"Voz {int(sid[1:])}"}
            for sid in speaker_ids
        ],
        "segments": segments,
        "models": models,
    }


def safe_diarize(audio: Path, manifest: dict, expected_speakers: int | None = None) -> dict:
    try:
        return diarize(audio, manifest, expected_speakers)
    except Exception as exc:
        return {
            "status": "unavailable",
            "count": expected_speakers if expected_speakers else None,
            "count_source": "user_hint" if expected_speakers else "unknown",
            "expected_speakers": expected_speakers,
            "speakers": [],
            "segments": [],
            "error": f"{type(exc).__name__}: {exc}",
        }
