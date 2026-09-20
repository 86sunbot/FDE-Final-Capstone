# Stage 10 - API, Component and Failure Design

## Primary use cases

| Endpoint/use case | Service | Authority |
|---|---|---|
| `GET /journeys/{id}` | Journey query | Authenticated read scope |
| `POST /identity/cases` | Identity service | Any permitted detector; no merge |
| `POST /identity/cases/{id}/decision` | Identity service | Simulated Identity Authority |
| `GET /readiness/{id}/{milestone}` | Readiness service | Deterministic, non-authoritative assessment |
| `POST /slots/reservations` | Command service | Authorized Planner |
| `POST /commands/{id}/reconcile` | Command service | Operations/Planner policy |
| `GET /quality/{batch}/packet` | Quality service | Read scope |
| `POST /quality/{batch}/release` | Quality service | Simulated Quality Authority only |
| `POST /recommendations` | Assistant gateway | Read/recommend; no command authority |

## Failure taxonomy

| Failure | Stable response/state | Recovery |
|---|---|---|
| Missing/contradictory prerequisite | `UNKNOWN` or `NOT_SATISFIED` | Owned evidence case |
| Unauthorized request | `AUTHORIZATION_DENIED` | Audit; no partial effect |
| Same idempotency key/different payload | `IDEMPOTENCY_CONFLICT` | New approved command/key |
| Timeout after possible effect | `OUTCOME_UNKNOWN` | Reconcile before retry |
| Source outage | Stale/unknown evidence with timestamp | Degraded read view and owner |
| Invalid assistant output | Deterministic-only response | Record rejection reason |
| Model outage | Deterministic-only response | No workflow outage |
| Corrupt/missing database | Health not ready | Restore/reseed; never invent state |

## Transaction boundaries

Command acceptance, payload binding, audit and outbox record share one local transaction. Approval validates current authority, exact proposal/payload and evidence version before appending its decision event. Projection updates are rebuildable from durable records.
