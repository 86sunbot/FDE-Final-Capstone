from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'data/manifest.json').read_text())
print(manifest['repo_name'])
print('version:', manifest['version'])
print('seed:', manifest['seed'])
print('dataset counts:')
for k,v in manifest['counts'].items(): print(f'  {k}: {v}')
print('\nStart with participant/CHALLENGE_BRIEF.md and docs/02_imperfection_layers.md')
