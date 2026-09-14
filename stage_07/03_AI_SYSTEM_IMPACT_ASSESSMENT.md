# Stage 7 - Preliminary AI System Impact Assessment

**Status:** PRELIMINARY FOR SYNTHETIC ACADEMIC POC  
**Decision:** AI is optional and disabled by default

## Intended AI function

AI may extract candidate facts from untrusted documents, summarize cited evidence, explain deterministic findings and propose non-binding next actions. It does not create canonical facts, resolve identity, satisfy a gate, approve a deviation, dispose product, release product, authorize clinical readiness or execute an external command.

## People and groups affected

| Group | Possible benefit | Possible harm | Required protection |
|---|---|---|---|
| Patient | Fewer coordination delays and clearer case state | Identity error, privacy loss, delayed or unsafe progression | Corroboration, data minimization, human authority, fail-closed gates |
| Treatment-center staff | Less manual reconciliation | Misleading confidence or extra alert burden | Evidence links, uncertainty display, usable override and escalation |
| Manufacturing/planning | Earlier impact visibility | Unsafe slot recommendation or duplicate action | Deterministic feasibility, idempotency, human command authority |
| Quality reviewers | Faster evidence-packet review | Automation bias or hidden missing evidence | Rules-only view, material citations, separation of recommendation and approval |
| Operations/support | Faster diagnosis | Opaque failures and unowned incidents | Trace IDs, bounded loops, runbooks and ownership |
| Organization | Better traceability and learning | False compliance, value or safety claim | Claim register, independent review and explicit limitations |

## Impact dimensions

### Safety and autonomy

The highest harm is a fluent output being mistaken for an authorized decision. The design response is structural: model output uses a separate recommendation type, cannot emit authority events and cannot call consequential tools. A human remains accountable and must inspect evidence.

### Privacy and confidentiality

The baseline is synthetic-sensitive. External providers and real personal/health data are denied by default. Future use requires approved purpose, minimization, access policy, retention, logging/redaction and supplier review. Prompt content and logs are treated as potential disclosure channels.

### Fairness and accessibility

The supplied synthetic data cannot demonstrate demographic representativeness or subgroup performance. The POC must not make fairness claims. Human-review interfaces should expose uncertainty, avoid color-only signals and permit keyboard-accessible evidence review; production testing remains pending.

### Transparency and contestability

Every material assertion must cite source, time and policy/rule version. Users can view the deterministic state, disagree, override within authority and open an owned case. AI wording never hides source conflicts.

### Reliability and resilience

AI failure must return the user to the deterministic workflow. Schema rejection, timeout, rate limiting and loop termination are explicit. Canonical state is reconstructable without the model.

### Environmental and cost impact

The POC records calls, tokens, latency and cost. It prefers deterministic computation for structured facts and does not send unchanged context repeatedly. No environmental benefit claim is made without measured data.

## Lifecycle controls

| Lifecycle point | Control |
|---|---|
| Data/knowledge intake | Trust tier, provenance, effective version and permissible-use check |
| Prompt assembly | Minimum necessary evidence; untrusted-content boundary; fixed authority policy |
| Model call | Approved provider/model only; timeout; token cap; no consequential tools |
| Output | Schema validation, citation verification, uncertainty and prohibited-action checks |
| Human review | Material evidence inspection, authority check and explicit decision |
| Operation | Drift, override, incident, cost and recommendation-quality monitoring |
| Change | Re-run full P0 suite and compare B/C before release |
| Retirement | Revoke access, dispose data/models/memory and preserve required audit evidence |

## Residual-impact position

Current residual risk is **not accepted** because no solution has been selected, built or tested. The Stage 7 result is a testable control hypothesis, not assurance. G4 must review actual TEVV results, human-factor evidence and any unresolved P0 failure.
