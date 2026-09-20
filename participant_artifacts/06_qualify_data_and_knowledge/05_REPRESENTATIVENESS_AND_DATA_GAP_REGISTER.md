# Stage 6 - Representativeness and Data-Gap Register

**Status:** Evidence-backed limitations; owners/closures pending  
**Last updated:** 2026-09-14

## 1. Observed synthetic coverage

| Dimension | Coverage |
|---|---|
| Patients/journeys | 800 synthetic records |
| Countries | 16 (`AE`, `AU`, `BE`, `CA`, `CH`, `DE`, `ES`, `FR`, `GB`, `IN`, `IT`, `JP`, `NL`, `SE`, `SG`, `US`) |
| Treatment centers | 24 synthetic centers |
| Manufacturing sites | 6 synthetic sites |
| Products | 3 synthetic therapy families/codes (`CGT-A1`, `CGT-B2`, `CGT-C3`) |
| Couriers | 5 synthetic providers |
| Enrollment period | 2026-01-06 through 2026-08-28 |
| Event occurrence period | 2026-01-06 through 2026-09-25 |
| DOB range | 1958-01-19 through 2007-03-15 |
| Supplied event types | 8 |
| Supplied evaluation/failure seeds | 6 evaluation cases and 10 injects |

Patient distribution is intentionally uneven: country counts range from 28 to 129; product counts are 285, 272 and 243; manufacturing site counts range from 124 to 150. This shows multi-site/multi-region shape but does not prove representative sampling.

## 2. Why production representativeness cannot be claimed

- All data is synthetic and generated for challenge signals, not sampled from actual operations.
- One generated cohort and short period cannot represent seasonality, policy change, product launch or rare-event tails.
- No actual clinical outcomes, patient harm, product disposition ground truth or human decision outcomes are supplied.
- No protected-group attributes or defensible fairness labels are supplied; names/country/DOB must not be used as proxies.
- One row per patient/consent/authorization/site snapshot omits natural longitudinal change.
- Failures are intentionally seeded, so prevalence is not an estimate of real production frequency.
- Email and shadow files are designed evidence, not a statistically complete record of human work.
- Sites/products/couriers are fictional; operational capacity and route realism are not externally validated.
- There is no train/validation/test split, sampling frame, missingness mechanism or independent annotation process.

## 3. Data and knowledge gap register

| Gap ID | Missing/insufficient evidence | Consequence | Required resolution | Needed by |
|---|---|---|---|---|
| GAP-001 | Authorized patient identity ground truth and corroboration policy | Cannot verify resolver accuracy or approve merges | Domain/identity owner supplies labelled relationships and review protocol | Stage 7/14 POC 1 |
| GAP-002 | COI/COC scans, transfer actors, locations and attestations | Matching strings cannot prove lineage/custody | Controlled event/evidence contract and synthetic golden fixtures | Stage 7/9 |
| GAP-003 | Consent effective, expiry, withdrawal and re-consent rules/artifacts | Milestone gate cannot be fully specified | Clinical/Legal controlled decision table and evidence schema | Stage 7/13 |
| GAP-004 | Clinical eligibility/readiness/conditioning rules and decisions | Cannot assert clinical progression | Clinical owner defines evidence and human authorization | Stage 7/13 |
| GAP-005 | Approved scheduling policy; current SOP is draft | Provisional reservation semantics are not authoritative | Policy owner approves/revises scheduling specification | Stage 8/13 |
| GAP-006 | Required QC assays, specifications, methods and explicit dispositions | Cannot interpret pending/OOS/OOT against release | Quality/Lab controlled specifications and golden decisions | Stage 7/14 POC 3 |
| GAP-007 | Blocking-deviation taxonomy, investigation evidence and valid links | Cannot determine release blocker/closure | Quality supplies blocking/disposition/closure rules and evidence | Stage 7/14 POC 3 |
| GAP-008 | Electronic approval/signature identity, meaning and SoD requirements | Cannot validate consequential approvals | Quality/Legal/Security specification | Stage 12/13 |
| GAP-009 | Thermal duration/profile method, sensor calibration and shipper integrity | Cannot determine product acceptability | Logistics/Quality controlled calculation/evidence fixtures | Stage 7/14 POC 3 |
| GAP-010 | Actual capacity constraints, change/cancel policy and external acknowledgements | Cannot prove realistic optimization/recovery | Manufacturing owner plus adapter contract/simulator | Stage 8/14 POC 2 |
| GAP-011 | Complete business event history and source sequencing | Cannot reconstruct all historical decisions | Target events and synthetic golden history; retain current gaps | Stage 9/14 |
| GAP-012 | Human task timestamps, touches, decisions, overrides and outcomes | Cannot measure task-time/adoption/automation bias baseline | Instrument controlled user study/simulation | Stage 7/15/19 |
| GAP-013 | Formulas/populations/windows for ten supplied KPIs | Before/after benefit claims remain non-reproducible | KPI owner supplies definitions or label as provided-only | Stage 7/19 |
| GAP-014 | Real geography/entity/regulatory/privacy context | Applicability remains preliminary | Legal/Regulatory/Privacy owner decision | Before real pilot |
| GAP-015 | Representative production sampling and drift history | No production generalization/drift claim | Approved data plan and monitoring cohort | Before real pilot |
| GAP-016 | Fairness/affected-group attributes and harm labels | Cannot quantify disparate impact | Impact assessment defines lawful measures and qualitative review | Stage 7/15 |
| GAP-017 | Source/provider availability, latency, throughput and incident logs | SLO/RTO/RPO not evidence-based | Load/fault test plus service-owner targets | Stage 7/16 |
| GAP-018 | Actual labor, delay, infrastructure, provider and token costs | TCO/value remain hypothetical | Cost data and measurement plan | Stage 8/19 |
| GAP-019 | Model/provider/version and labelled AI task ground truth | Cannot select/evaluate AI | Provider options plus blinded golden/rubric set | Stage 7/8 |
| GAP-020 | Retention, legal hold, correction/deletion and records schedules | Data lifecycle cannot be implemented safely | Legal/Privacy/Records policy | Stage 9/12/16 |

## 4. Gap disposition rules

Each gap must be one of:

- `CLOSE_WITH_EVIDENCE` - obtain an approved specification/dataset/decision.
- `SIMULATE_EXPLICITLY` - create a synthetic fixture labelled as an assumption, not source fact.
- `DESIGN_FOR_UNKNOWN` - fail closed, abstain or route to a human.
- `ACCEPT_RESIDUAL` - accountable owner accepts bounded residual risk.
- `REMOVE_SCOPE` - remove a capability/claim that cannot be supported.

Never close a gap by inferring ground truth from the same conflicting dataset being evaluated.

## 5. Proposed evaluation sampling approach

- Keep the supplied six cases and ten injects as mandatory immutable seeds.
- Add stratified synthetic cases across product, country/site, phase and exception type.
- Add normal and near-boundary cases to measure false blocks, not only dramatic failures.
- Separate rule development fixtures from a held-out acceptance set.
- Use authorized expert labels for consequential decisions; Codex-generated labels are hypotheses.
- Test invariants with property-based generation and targeted adversarial mutations.
- Report results per case family and counter-metric; do not extrapolate synthetic percentages to real populations.

## 6. Readiness conclusion

The data supports a robust synthetic POC and evaluation harness. It does not support production validation, predictive generalization or real-world benefit claims. The recommended solution therefore emphasizes deterministic invariants, explicit unknowns, human authorization and reversible local simulation.
