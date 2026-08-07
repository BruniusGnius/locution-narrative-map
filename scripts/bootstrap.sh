#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "--help" ]; then
  echo "Usage: bash scripts/bootstrap.sh [--dry-run]"
  exit 0
fi

DRY_RUN=0
if [ "${1:-}" = "--dry-run" ]; then DRY_RUN=1; fi

case "$(uname -s)" in
  Darwin|Linux) ;;
  *) echo "Unsupported shell platform. On Windows use scripts/bootstrap.ps1" >&2; exit 2 ;;
esac

HOME_BASE="${HOME:-.}"
RUNTIME_HOME="${LNM_HOME:-$HOME_BASE/.local/share/locution-narrative-map}"
UV_DIR="$RUNTIME_HOME/uv"
UV_BIN="$UV_DIR/uv"
VENV="$RUNTIME_HOME/venv"
PYTHON_DIR="$RUNTIME_HOME/python"
CACHE_DIR="$RUNTIME_HOME/cache"
BIN_DIR="$RUNTIME_HOME/bin"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$UV_DIR" "$PYTHON_DIR" "$CACHE_DIR" "$BIN_DIR"

export UV_PYTHON_INSTALL_DIR="$PYTHON_DIR"
export UV_CACHE_DIR="$CACHE_DIR/uv"
export HF_HOME="$CACHE_DIR/huggingface"
export XDG_CACHE_HOME="$CACHE_DIR/xdg"
export UV_NO_MODIFY_PATH=1

if [ "$DRY_RUN" -eq 1 ]; then
  echo "runtime_home=$RUNTIME_HOME"
  echo "platform=$(uname -s) arch=$(uname -m)"
  echo "would_install_uv=$UV_BIN"
  echo "would_create_venv=$VENV"
  if [ "$(uname -s)" = "Darwin" ] && [ "$(uname -m)" = "arm64" ]; then
    echo "backend=mlx"
  else
    echo "backend=faster-whisper"
  fi
  exit 0
fi

# Fast path: an existing healthy runtime should not reinstall anything.
if [ -x "$VENV/bin/python" ] && [ -f "$RUNTIME_HOME/runtime.json" ]; then
  if "$VENV/bin/python" "$SCRIPT_DIR/doctor.py" --home "$RUNTIME_HOME" >/dev/null 2>&1; then
    echo "Locution Narrative Map runtime: OK"
    exit 0
  fi
fi

if [ ! -x "$UV_BIN" ]; then
  if ! command -v curl >/dev/null 2>&1; then
    echo "Cannot download the local runtime because curl is unavailable." >&2
    exit 3
  fi
  echo "Preparing local runtime..."
  curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="$UV_DIR" UV_NO_MODIFY_PATH=1 sh
fi

"$UV_BIN" venv --python 3.12 "$VENV"
PY="$VENV/bin/python"
"$UV_BIN" pip install --python "$PY" "imageio-ffmpeg==0.6.0"

BACKEND="faster-whisper"
if [ "$(uname -s)" = "Darwin" ] && [ "$(uname -m)" = "arm64" ]; then
  BACKEND="mlx"
  "$UV_BIN" pip install --python "$PY" "mlx-whisper==0.4.3"
else
  "$UV_BIN" pip install --python "$PY" "faster-whisper==1.2.1"
fi

"$PY" "$SCRIPT_DIR/configure_runtime.py" --home "$RUNTIME_HOME" --backend "$BACKEND"
"$PY" "$SCRIPT_DIR/doctor.py" --home "$RUNTIME_HOME"
