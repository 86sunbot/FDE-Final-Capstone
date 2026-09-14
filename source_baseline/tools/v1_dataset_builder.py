# This script intentionally delegates to the already-distributed snapshot rather than mutating participant evidence.
# To create a new synthetic release, copy the repo, modify deterministic generation logic, and version it as v2.
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'data/manifest.json').read_text())
print('v1 is immutable by design for assessment reproducibility.')
print('seed:',m['seed'],'patients:',m['counts']['patients'])
print('Create a versioned v2 generator rather than rewriting v1 evidence in place.')
