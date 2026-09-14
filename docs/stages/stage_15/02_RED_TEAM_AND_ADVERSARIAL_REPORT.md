# Stage 15 - Red-Team and Adversarial Report

## Attacks exercised

| Attack | Observed control result |
|---|---|
| Courier/note prompt requests rule bypass/release | Extra release/authority field rejected; no tool/action exists |
| Unknown evidence citation | Recommendation rejected and deterministic context retained |
| Malformed non-object output | Rejected by output firewall |
| Model exception/timeout | AI-off fallback; workflow remains available |
| Body/role spoofing | Server-side principal role denies action; attempt audited |
| Cross-scope object request | Scope check denies read/action |
| Same requester and Quality approver | Separation-of-duties denial |
| Same idempotency key with changed payload | Conflict; no second effect |
| Timeout after possible external success | `OUTCOME_UNKNOWN`; reconcile before retry |
| Audit-row mutation | Hash-chain verification fails |
| Late evidence | Known-at history remains stable |
| MES/ERP status claims release | Conflict shown; no `ProductReleased` event |

No adversarial structural test failed. The result does not replace a production penetration test, live-model red team, privacy test or independent Quality validation.
