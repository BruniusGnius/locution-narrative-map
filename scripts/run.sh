#!/usr/bin/env bash
set -euo pipefail
RUNTIME_HOME="${LNM_HOME:-${HOME:-.}/.local/share/locution-narrative-map}"
PY="$RUNTIME_HOME/venv/bin/python"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -x "$PY" ]; then
  bash "$SCRIPT_DIR/bootstrap.sh"
fi
exec "$PY" "$SCRIPT_DIR/cli.py" --home "$RUNTIME_HOME" "$@"
