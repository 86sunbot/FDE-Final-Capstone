# V2 Verification Evidence

Verification was executed from the repository root using the packaged source tree.

## Release checks
- Repository structural verifier: **VERIFY_OK**
- Python compile/import smoke check: **PASS**
- API module import: **PASS** (`cgt_orchestrator.api:app`)
- SQLite `PRAGMA integrity_check`: **PASS** (performed by `scripts/verify_repo.py`)
- JSON parse and CSV rectangularity checks: **PASS**
- Restricted-role/reference scan: **PASS — zero matches**
- External consequential-control integration: **disabled / not configured**

## Test result
```text
.xxx.                                                                    [100%]
2 passed, 3 xfailed in 0.08s
```
Expected-failure tests document deliberately preserved legacy limitations; they are not accidental release failures.

## Diagnostic evidence
- `patient_count`: **800**
- `duplicate_mrn_count`: **2**
- `impossible_shipment_time_count`: **9**
- `mes_qms_conflict_count`: **16**
- `slot_state_conflict_count`: **9**
- `withdrawn_consent_count`: **5**
- `expired_or_due_site_controls`: **6**

## File authentication
`checksums.sha256` contains SHA-256 hashes for the release files. These hashes provide reproducible integrity evidence; this release is not digitally signed and does not claim regulatory certification.
