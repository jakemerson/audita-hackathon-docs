#!/usr/bin/env bash
set -euo pipefail

AUDITA_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$AUDITA_DIR"

if [[ ! -x .venv/bin/python ]]; then
  command -v python3.12 >/dev/null 2>&1 || { echo "Python 3.12 não encontrado." >&2; exit 1; }
  python3.12 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi

exec .venv/bin/python start.py "$@"
