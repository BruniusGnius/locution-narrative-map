#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def check_import(name: str) -> tuple[bool, str]:
    try:
        __import__(name)
        return True, "ok"
    except Exception as exc:  # diagnostic tool
        return False, f"{type(exc).__name__}: {exc}"


def run_doctor(home: Path) -> dict:
    manifest_path = home / "runtime.json"
    report = {"ok": True, "home": str(home), "checks": {}}
    if not manifest_path.exists():
        report["ok"] = False
        report["checks"]["manifest"] = "missing"
        return report

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report["checks"]["manifest"] = "ok"
    backend = manifest.get("backend")
    ffmpeg = Path(manifest.get("ffmpeg", ""))
    if ffmpeg.exists():
        try:
            p = subprocess.run([str(ffmpeg), "-version"], capture_output=True, text=True, timeout=10)
            report["checks"]["ffmpeg"] = "ok" if p.returncode == 0 else "failed"
            report["ok"] &= p.returncode == 0
        except Exception as exc:
            report["checks"]["ffmpeg"] = f"failed: {exc}"
            report["ok"] = False
    else:
        report["checks"]["ffmpeg"] = "missing"
        report["ok"] = False

    module = "mlx_whisper" if backend == "mlx" else "faster_whisper"
    ok, detail = check_import(module)
    report["checks"]["transcription_backend"] = detail
    report["ok"] &= ok
    report["backend"] = backend
    report["python"] = sys.version.split()[0]
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    report = run_doctor(Path(args.home).expanduser().resolve())
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Locution Narrative Map doctor")
        for key, value in report["checks"].items():
            print(f"- {key}: {value}")
        print(f"- backend: {report.get('backend', 'unknown')}")
        print("Status: OK" if report["ok"] else "Status: NEEDS REPAIR")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
