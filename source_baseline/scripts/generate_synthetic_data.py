"""Regeneration entry point.

The distributed v1 repository already includes deterministic generated data. For workshop reproducibility,
this script verifies the seed and provides a safe path to rebuild via `scripts/regenerate_v1.py`.
"""
import argparse, json
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument('--seed',type=int,default=42001); p.add_argument('--patients',type=int,default=800); a=p.parse_args()
if a.seed != 42001 or a.patients != 800:
    raise SystemExit('v1 deterministic snapshot supports --seed 42001 --patients 800. Modify scripts/regenerate_v1.py for a new version.')
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'data/manifest.json').read_text())
print(f"Synthetic v1 snapshot already present: seed={m['seed']} patients={m['counts']['patients']}")
print('Use scripts/regenerate_v1.py to rebuild the exact snapshot.')
