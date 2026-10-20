#!/usr/bin/env bash
# Create (or refresh) the tooling environment used to execute lessons.
#   ensure_env.sh [python-executable]      # default: python3 ; use the NEWEST Python you have
# Creates <repo>/.course-tools/venv with nbclient, nbformat, ipykernel and the course requirements.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
PY="${1:-python3}"
VENV="$ROOT/.course-tools/venv"
REQ="$ROOT/Python-Mastery-Website/Python-Mastery-Course/requirements.txt"
"$PY" -m venv "$VENV"
"$VENV/bin/python" -m pip install --quiet --upgrade pip
"$VENV/bin/python" -m pip install --quiet nbclient nbformat ipykernel
[ -f "$REQ" ] && "$VENV/bin/python" -m pip install --quiet -r "$REQ" || true
"$VENV/bin/python" -c "import sys; print('tooling env ready:', sys.executable, sys.version.split()[0])"
