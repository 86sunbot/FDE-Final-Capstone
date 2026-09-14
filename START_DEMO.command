#!/bin/zsh
set -euo pipefail

repo_dir="${0:A:h}"
cd "$repo_dir"

if [[ ! -x .venv/bin/python ]]; then
  echo "Creating the local Python environment..."
  python3 -m venv .venv
fi

echo "Installing verified demo dependencies..."
.venv/bin/pip install -e '.[dev,api]'

mkdir -p runtime
echo "Starting CGT Control Tower at http://127.0.0.1:8000"
echo "Keep this window open. Press Control-C to stop the app."

(sleep 1; open "http://127.0.0.1:8000") &
FDE_DB=runtime/control-tower.db AI_MODE=off PYTHONPATH=src \
  exec .venv/bin/python -m uvicorn fde_capstone.api:app --host 127.0.0.1 --port 8000
