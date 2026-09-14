# Data Map

| Dataset | Purpose | Typical forensic concerns |
|---|---|---|
| patients / CRM / clinical exports | patient identity & current status | duplicate IDs, DOB/MRN/center disagreement |
| collections | source material | COI, bag, viability, collection timing |
| shipments | outbound/return logistics | custody, sequencing, temperature, status |
| cryogenic_telemetry | sensor stream | missing points, quality, excursions |
| manufacturing_slots | capacity reservation | scheduler vs MES state conflict |
| batches | manufacturing / release state | MES vs ERP vs QMS semantics |
| qc_results | assays | pending/OOT/OOS/asynchronous reporting |
| deviations | quality exceptions | open investigations, weak linkage |
| consents | consent lifecycle | versioning, withdrawal, validity |
| authorizations | reimbursement | pending/conditional/denied states |
| events.jsonl | cross-system event history | duplicate, delayed, recorded vs occurred time |
| shadow_ops | human workarounds | stale applications, decisions outside systems |
