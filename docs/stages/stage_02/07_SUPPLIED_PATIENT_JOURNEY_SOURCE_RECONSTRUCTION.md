# Stage 2 — Supplied Patient Journey/State Reconstruction

**Scope:** six v2 synthetic EVAL patients only, frozen read-only source assertions. This closes the *academic example* of client deliverable 2; it does not reconstruct all 800 journeys into a governed current-state platform. The general brownfield process and systems are in [the current-state architecture](03_CURRENT_STATE_PROCESS_AND_ARCHITECTURE.md); the domain/authority model is in Stage 5.

The implementation in `src/fde_capstone/source_cases.py::reconstruct_source_journey` orders each patient's source timestamps and retains file/row locators. The API returns it inside `/api/source/cases/{case_id}`, and the browser **Source case → Inspect case** panel shows a collapsible event sequence. No source file is changed and no identity link, custody verification, release or clinical decision is inferred.

| Supplied case | Patient | Source-level finding retained | What remains unverified |
|---|---|---|---|
| EVAL-001 | P-00001 | Declared patient/collection/shipment/batch IDs match; 17 timed source assertions | Repeated COI strings are not custody attestations; stored `journey_status` is not an approved transition |
| EVAL-002 | P-00079 | CRM and clinical DOB disagree | Identity authority must corroborate; no silent merge |
| EVAL-003 | P-00083 | A shipment arrival precedes departure | Sorting timestamps does not repair the record or establish causal state |
| EVAL-004 | P-00157 | Consent source says withdrawn | Downstream continuation is blocked pending controlled current-consent review |
| EVAL-005 | P-00201 | Source state remains visible | QMS outage is evaluation stimulus, not an observed outage or tested degraded-mode history |
| EVAL-006 | P-00301 | Source state remains visible | Courier-note attack is evaluation stimulus, not an authenticated courier instruction |

Each case currently has 17 timed observations from enrollment, consent, payer, collection, slot, shipment, MES and QC source rows. Batch `MES`, `ERP` and `QMS` labels, patient journey labels, current consent/payer statuses and slot states are **separate source snapshot assertions**; they are deliberately not attached to earlier timestamps, because that would invent historical transitions. The gate vector therefore keeps identity unadjudicated or conflicted, lineage/COC unverified, Quality release unknown without an authorized Quality event, and clinical readiness unknown without controlled evidence. A withdrawn consent is an explicit blocker.

**Known-at limitation:** the raw package supplies event timestamps but not a complete recorded-at/ingest history. This sequence is occurrence-time order only, not a bitemporal replay or present-tense medical/manufacturing truth. Stage 6 records the missing ground truth and policy; Stage 15 grades only narrower test properties. Trace: `REQ-SRC-001/002/003`, `tests/test_source_cases.py`, `tests/test_api_surface.py`.
