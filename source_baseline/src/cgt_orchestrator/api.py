try:
    from fastapi import FastAPI, HTTPException
except ImportError as exc:  # optional dependency
    raise RuntimeError("Install requirements.txt to run the API") from exc

from .repository import LegacyRepository
from .legacy.status_rules import patient_ready

app = FastAPI(title="Synthetic CGT Brownfield API", version='2.0.0')
repo = LegacyRepository()

@app.get('/health')
def health():
    return {'status':'ok','synthetic':True}

@app.get('/patients/{patient_key}/journey')
def journey(patient_key: str):
    data=repo.journey(patient_key)
    if not data['patient']:
        raise HTTPException(404, 'patient not found')
    return data

@app.get('/exceptions')
def exceptions():
    return {'open_deviations': repo.open_deviations()}

@app.get('/legacy/readiness/{patient_key}')
def legacy_readiness(patient_key: str):
    data=repo.journey(patient_key)
    if not data['patient']:
        raise HTTPException(404, 'patient not found')
    batch=data['batches'][0] if data['batches'] else None
    return {'patient_key':patient_key,'ready':patient_ready(data['patient'],batch),'warning':'legacy heuristic; not a validated clinical/quality decision'}
