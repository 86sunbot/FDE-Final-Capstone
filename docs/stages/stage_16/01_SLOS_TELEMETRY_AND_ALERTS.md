# Stage 16 - SLOs, Telemetry and Alerts

**Scope:** Proposed for a local simulated service; production SLOs are not approved.

| Signal/SLO | Local target | Alert/response |
|---|---:|---|
| Health/readiness | 100% during demo window | Stop demonstration; inspect database/migration |
| P0 unauthorized accepted action | 0 | Immediate stop, preserve evidence, open P0 incident |
| Duplicate external effect | 0 | Disable command adapter; reconcile all unknown commands |
| Unowned P0 case | 0 | Page simulated operations owner |
| Audit-chain failure | 0 | Freeze mutations; preserve copy; investigate tampering/corruption |
| Deterministic projection | p95 <=250 ms in defined local benchmark | Profile; do not claim production capacity |
| Unknown command outcome | 100% owned/reconciled before retry | Alert per command and aging threshold |
| AI fallback | Workflow availability 100% | Keep AI off; investigate provider separately |
| Recommendation citation/schema rejection | 100% rejected safely | Record reason and inspect trend |
| Source freshness/drift | Visible per source | Mark affected projection unknown/stale |

Every command, case, decision and recommendation has a correlation ID. Metrics count accepted commands, replay, idempotency conflicts, unknown outcomes, reconciliations, denials, recommendations and fallbacks. Logs must not include secrets or unnecessary sensitive raw payloads.
