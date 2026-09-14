# Stage 5 - Business Rules and Decision Tables

**Status:** Draft specification; domain/Quality approval pending  
**Last updated:** 2026-09-14

## 1. Rule semantics

Each evaluation returns one of:

- `SATISFIED` - required evidence proves the prerequisite under the selected policy version.
- `NOT_SATISFIED` - evidence proves the prerequisite failed.
- `UNKNOWN` - evidence is absent, unusable, stale, contradictory or lacks required authority.
- `NOT_APPLICABLE` - the selected controlled policy states the prerequisite does not apply.

For P0/consequential progression, only `SATISFIED` clears the prerequisite. `UNKNOWN` fails closed and creates/updates an owned exception.

## 2. Cross-domain rules

| Rule ID | Requirement | Source basis | Authority | Failure behavior |
|---|---|---|---|---|
| BR-EVD-001 | Preserve raw value, source record, occurred/effective and recorded time for every decision-relevant assertion | Challenge non-negotiables | Data owner | Reject/quarantine malformed assertion; do not invent value |
| BR-EVD-002 | Canonical projection must cite facts, decisions and rule/policy versions | Target capability | Journey owner | Return `UNKNOWN`/incomplete evidence |
| BR-ID-001 | No identity or lineage relation may be created solely from one ambiguous identifier or model score | Challenge AGENTS.md | Clinical/identity authority | Abstain and open identity case |
| BR-ID-002 | MRN is not globally unique | Two duplicated MRN groups | Identity authority | Namespace and corroborate; conflict if ambiguous |
| BR-STATE-001 | Only an allowed transition with satisfied guards may change canonical state | Engineering expectation | Domain owner | Reject transition and audit attempt |
| BR-TIME-001 | Occurred and recorded time must remain distinct | Challenge AGENTS.md | Data owner | Quarantine invalid envelope; projection retains prior known state |
| BR-CMD-001 | An idempotency key binds one canonical payload and command type/scope | Retry duplicate evidence | Service owner | Same payload returns prior result; different payload returns conflict |
| BR-CMD-002 | External timeout/unknown acknowledgement is not success or failure | Partial-transaction risk | Service owner | Persist `OUTCOME_UNKNOWN`; reconcile before retry/compensation |
| BR-AUTH-001 | Authority derives from authenticated principal and server policy | Stage 4 policy | Security/business authority | Deny and audit |
| BR-AUTH-002 | Recommendation, approval and execution are separate events | Stage 4 policy | Business authority | No state change from recommendation |
| BR-AI-001 | AI output never establishes identity, lineage, disposition, release or clinical readiness | Challenge/Stage 4 | QA/Clinical/Security | Refuse/escalate; deterministic evidence view remains |

## 3. Identity/lineage decision table

| Relevant assertions | Corroboration | Material conflict | Authorized resolution | Result |
|---|---|---|---|---|
| Missing | Any | Any | No | `UNKNOWN`; open case |
| Present | Insufficient | No | No | `UNKNOWN`; request evidence |
| Present | Sufficient under approved policy | No | Not required by policy | `SATISFIED` for the named relationship only |
| Present | Any | Yes | No | `CONFLICT`; open/retain case; no merge |
| Present | Any | Yes | Approved with reason/evidence | Apply versioned relationship decision; retain conflicting assertions |
| Present | Any | Any | Rejected | Do not apply relationship; record reason |

The challenge does not supply an approved matching policy. Therefore, “sufficient corroboration” remains an unresolved controlled specification, not code inferred from the sample.

## 4. Provisional scheduling decision table

SOP-SCHED-003 v2 is marked **Draft**, so this table is a policy hypothesis and cannot be a production rule until approved.

| Identity/COI evidence | Site controls | Authorization | Capacity feasible | Decision |
|---|---|---|---|---|
| Conflict/unknown for required scope | Any | Any | Any | Block; identity/site case as applicable |
| Satisfied | Satisfied | Approved | Yes | Reservation permitted under normal policy |
| Satisfied | Satisfied | Pending/conditional | Yes | Provisional reservation only if approved policy explicitly permits; revalidation required |
| Satisfied | Satisfied | Denied/withdrawn/expired | Any | Do not create/continue normal reservation; human commercial/clinical review |
| Satisfied | Failed/unknown | Any | Any | Block relevant downstream milestone; provisional planning policy unresolved |
| Satisfied | Satisfied | Any | No | No reservation; calculate feasible alternatives |

## 5. Command/idempotency decision table

| Existing key | Payload digest | Stored command state | Response/action |
|---|---|---|---|
| No | New | N/A | Persist command before dispatch; execute once |
| Yes | Same | Completed | Return stored result; no additional side effect |
| Yes | Same | In progress | Return/observe current command; do not dispatch another |
| Yes | Same | Outcome unknown | Reconcile external state; do not blindly retry |
| Yes | Same | Failed retryable | Retry according to bounded policy and attempt limit |
| Yes | Different | Any | `IDEMPOTENCY_CONFLICT`; no side effect; audit/escalate |

## 6. Quality-release prerequisite table

SOP-QA-014 v4 establishes that manufacturing completion is not product release and that release requires required QC evidence, disposition of blocking deviations and authorized electronic approval.

| Manufacturing evidence | Required QC evidence/disposition | Blocking deviation disposition | Authorized Quality approval | Quality release result |
|---|---|---|---|---|
| Missing/unknown | Any | Any | Any | `UNKNOWN`; cannot release |
| Complete | Missing/pending/unknown | Any | Any | `NOT_SATISFIED` or `UNKNOWN`; cannot release |
| Complete | Satisfied | Open/unknown blocking status | Any | `UNKNOWN`; Quality review required |
| Complete | Satisfied | All blocking deviations dispositioned | Missing/invalid | `NOT_SATISFIED`; cannot release |
| Complete | Satisfied | All blocking deviations dispositioned | Valid and bound to exact evidence | `RELEASED` decision may be recorded |

The supplied data does not identify required assays or which deviations are blocking. Those rules must be supplied by Quality; the system must not infer them from status, severity or frequency.

## 7. Thermal evidence decision table

SOP-LOG-007 v7 supersedes v6. A point above `-120 °C` is not itself a disposition decision.

| Profile availability | Sensor/data quality | Duration/cumulative profile | Shipper integrity | Quality review | Result |
|---|---|---|---|---|---|
| Missing/incomplete | Any | Any | Any | Any | `UNKNOWN`; open evidence case |
| Present | Warning/invalid | Any | Any | Any | `UNKNOWN`; investigate sensor/evidence quality |
| Present | Acceptable | Not calculated under controlled method | Any | Any | `UNKNOWN`; calculate approved features |
| Present | Acceptable | Calculated | Missing/unknown | Any | `UNKNOWN`; request integrity evidence |
| Present | Acceptable | Calculated | Known | Pending | `AWAITING_QUALITY_DISPOSITION` |
| Present | Acceptable | Calculated | Known | Authorized disposition | Record the human decision; AI does not determine acceptance |

No new temperature/duration acceptance threshold is introduced by this capstone.

## 8. Journey milestone assessment

| Milestone | Required prerequisite categories | Clear condition | Known gaps |
|---|---|---|---|
| Collection scheduling | Identity, consent, clinical eligibility, site capability | Every policy-required item `SATISFIED` | Clinical eligibility/source rules absent |
| Collection execution | Above plus effective consent/site revalidation and collection order | Every required item `SATISFIED` at execution time | Exact order/approval semantics absent |
| Manufacturing reservation | Identity/lineage scope, site/capacity, authorization policy | Normal/provisional decision table result permits | Draft scheduling SOP not approved |
| Manufacturing start | Verified input material/COI, delivered outbound custody, valid reservation | All guards satisfied | Full MES/material genealogy unavailable |
| Quality release | Manufacturing evidence, required QC, blocking deviation disposition, authorized Quality approval | Explicit `QualityReleaseDecision=APPROVED` | Assay/blocking/signature policy absent |
| Return shipment | Released/authorized product plus route/custody controls per policy | Controlled policy decision | Exact pre-release shipping policy absent |
| Conditioning/infusion readiness | Correct released product received, COI/COC, viability/thermal disposition, current patient/site/clinical prerequisites | Every required item satisfied and clinical authorization recorded | Clinical readiness rules absent |

## 9. Rule-change control

Every controlled rule must have an immutable ID, semantic version, status (`DRAFT`, `EFFECTIVE`, `SUPERSEDED`, `RETIRED`), effective interval, accountable owner, source specification, tests and change record. Projection and decision records bind the exact rule versions used.
