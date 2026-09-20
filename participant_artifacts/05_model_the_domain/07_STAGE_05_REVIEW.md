# Stage 5 - Internal Domain-Model Review

**Review type:** Codex internal consistency check; not domain-owner approval  
**Status:** READY FOR REVIEW; academic G1 approved; domain-owner review pending  
**Review date:** 2026-09-14

## 1. Stage objective

Create one shared business and decision vocabulary that preserves source evidence, defines bounded ownership and makes safety-critical rules/events/states explicit before architecture or implementation selection.

## 2. Artifact review

| Required artifact | Evidence | Internal result |
|---|---|---|
| Canonical glossary | `01_DOMAIN_GLOSSARY.md` | PASS |
| Capability and bounded-context map | `02_CAPABILITY_BOUNDED_CONTEXT_AND_CONTEXT_MAP.md` | PASS |
| Aggregates and ownership | `03_AGGREGATES_OWNERSHIP_AND_AUTHORITY.md` | PASS |
| Attribute/decision authority | `03_AGGREGATES_OWNERSHIP_AND_AUTHORITY.md` | PASS; human owners pending |
| Business rules and decision tables | `04_BUSINESS_RULES_AND_DECISION_TABLES.md` | PASS; controlled policies pending |
| Domain event/temporal model | `05_DOMAIN_EVENTS_AND_TEMPORAL_MODEL.md` | PASS |
| Canonical state machines | `06_CANONICAL_STATE_MACHINES.md` | PASS; domain approval pending |
| Machine-readable domain specification | `domain_spec.json` | PASS |
| Specification validator/tests | `../tools/validate_domain_spec.py`; `../tests/test_domain_spec.py` | PASS |

## 3. Executable verification

Commands run from the capstone root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/validate_domain_spec.py docs/stages/stage_05/domain_spec.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_domain_spec.py
```

Final result:

- Specification validator: `PASS`.
- Rules: `11`.
- Event types: `53`.
- State machines: `4`.
- Transitions: `52`.
- Domain safety tests: `5 passed`.

The first validator run correctly failed because `AuthorizationDenied` was referenced by a transition but absent from the event catalogue. The catalogue was corrected and all checks rerun. This failure/fix is retained as evidence that the validator detects cross-specification drift.

## 4. Safety-invariant checks

| Invariant | Result |
|---|---|
| Quality `APPROVED` has exactly one path, through authorized `ProductReleased` | PASS |
| MES/ERP status cannot directly establish Quality release | PASS |
| Identity `APPROVED` has exactly one authorized decision path | PASS |
| AI recommendation is not a domain state transition | PASS |
| Same-key/different-payload command is rejected before dispatch | PASS |
| Occurred/recorded time and evidence/provenance are mandatory in canonical envelope | PASS |
| Original source ZIP remains unchanged | PASS; SHA-256 `74d31dc4694d52b0e9a9fb337e6ccda1086ad430b19287f9ca2b4b4e650ca979` |

## 5. Human decisions required

1. Approve G1 before formally entering Stage 5.
2. Confirm or revise glossary terms and bounded-context ownership.
3. Assign actual attribute and decision authorities.
4. Supply approved identity matching/corroboration policy.
5. Approve milestone-specific consent, authorization and site rules.
6. Supply required QC assay, blocking deviation and disposition taxonomy.
7. Confirm cancellation, discontinuation, rework and remanufacture transitions.
8. Confirm signature/separation-of-duties requirements.
9. Confirm event timestamp, correction and retention policy.

## 6. Exit assessment

The draft meets internal structural and safety checks, but Stage 5 cannot be labelled `READY FOR REVIEW` under the programme sequence until G1 is approved. After G1, the same package requires accountable domain-owner validation; any changes must update the machine specification and tests together.

## 7. Next safe action

Obtain the G1 decision. In parallel, Stage 6 data-quality and lineage profiling may be prepared as discovery evidence, but no domain rule or architecture is approved by that preparation.
