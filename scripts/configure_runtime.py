#!/usr/bin/env python3
import argparse
import json
import os
import platform
import shutil
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", required=True)
    ap.add_argument("--backend", required=True, choices=["mlx", "faster-whisper"])
    args = ap.parse_args()

    home = Path(args.home).expanduser().resolve()
    bin_dir = home / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    import imageio_ffmpeg

    source = Path(imageio_ffmpeg.get_ffmpeg_exe()).resolve()
    target = bin_dir / ("ffmpeg.exe" if os.name == "nt" else "ffmpeg")
    if target.exists() or target.is_symlink():
        target.unlink()
    try:
        target.symlink_to(source)
    except OSError:
        shutil.copy2(source, target)
    if os.name != "nt":
        target.chmod(0o755)

    manifest = {
        "version": 1,
        "backend": args.backend,
        "platform": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "home": str(home),
        "ffmpeg": str(target),
        "models": {
            "mlx": {
                "fast": "mlx-community/whisper-small-mlx",
                "balanced": "mlx-community/whisper-turbo",
                "quality": "mlx-community/whisper-large-v3-mlx",
            },
            "faster-whisper": {
                "fast": "small",
                "balanced": "medium",
                "quality": "large-v3",
            },
        },
    }
    (home / "runtime.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Runtime ready: {home}")
    print(f"Backend: {args.backend}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
