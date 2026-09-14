# Stage 12 - Supplier, SBOM, AIBOM and Exit Plan

## Supplier decision

No AI or SaaS supplier is selected. The POC operates with AI off or a deterministic fake adapter. Therefore provider security, privacy, residency, subprocessor, model-training, retention, uptime, quality agreement and exit claims are **not applicable yet**, not passed.

## SBOM scope

The application uses Python standard library at its core. FastAPI/Uvicorn are optional demo-API dependencies. `requirements.txt` pins permitted ranges; `stage_14/SBOM.json` is generated from the installed environment used for verification and is not a signed production SBOM.

## AIBOM

| Item | Value |
|---|---|
| AI component | Optional bounded recommendation gateway |
| Live model/provider | None selected |
| CI evaluator | Deterministic fake and adversarial fixtures |
| Training/fine-tuning | None |
| Vector store/embedding | None |
| Long-term model memory | None |
| Tools | Read-only scoped context; no consequential tools |
| Output contract | `recommendation.schema.json` |

## Exit/kill plan

Set AI mode off, remove provider configuration, revoke any future credential, stop sending contexts, retain required audit metadata, delete disposable prompt/output caches under the approved retention rule and continue deterministic O2 operation. The domain/events/database do not depend on provider-native structures.

## Production supplier questions

Before any live model use: approve intended purpose and data categories; assess data location/retention/training; security and incident terms; availability and change notice; model/version pinning; evaluation access; subcontractors; audit evidence; portability; deletion; pricing; regulated-quality responsibilities and termination assistance.
