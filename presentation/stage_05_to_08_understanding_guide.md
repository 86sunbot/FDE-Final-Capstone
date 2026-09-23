# Stages 5–8: plain-language understanding guide

## The capstone context

The capstone coordinates a patient-specific Cell and Gene Therapy journey when the systems involved disagree or do not contain enough evidence.

The simplified journey is:

**Patient identified → readiness checked → material collected → transported → manufactured → Quality reviewed → product returned → infusion readiness confirmed**

The main systems contribute different evidence:

| Source | Contribution |
|---|---|
| Clinical | Patient information, consent and readiness |
| Scheduling | Slots and reservations |
| MES | Manufacturing progress |
| LIMS | Laboratory results |
| QMS | Deviations, Quality decisions and release evidence |
| ERP | Inventory and related business information |
| Logistics and sensors | Movement, custody and temperature evidence |
| Emails and spreadsheets | Informal coordination and exception information |

These sources can disagree. “Manufacturing complete” or “inventory available” does not by itself mean that a product is released. Release requires the right evidence and an authorised Quality decision.

The source package is synthetic training data. It supports an academic proof of concept and does not prove that a real facility was visited or that real operators were interviewed.

## What Stages 1–4 established

| Stage | Question | Output |
|---|---|---|
| 1 | What are we improving, and who owns decisions? | Mandate, scope, stakeholders and provisional responsibilities |
| 2 | How does the current operation work? | Process maps, system views, dependencies and brownfield findings |
| 3 | What causes the problems and what matters? | Problem framing, root causes, KPIs, CTQs and value hypothesis |
| 4 | Is this use case suitable, and where could AI help? | Regulatory screen, non-AI alternative, AI suitability and Gate 1 |

Gate 1 allowed continued synthetic academic POC work. It did not approve production, regulatory use or autonomous decisions.

## Stage 5 — Model the domain

Stage 5 defines what the business terms, decisions and status changes mean.

### Domain glossary

The glossary defines the key journey objects:

- **Patient:** the person receiving the therapy.
- **Collection:** starting material collected from that patient.
- **Shipment:** physical movement of collection material or manufactured product.
- **Manufacturing batch:** the patient-specific manufacturing execution unit.
- **Quality release:** an authorised decision that release prerequisites are satisfied.

The important relationship is:

**Patient → collection → shipment → manufacturing batch → Quality release → return shipment → treatment**

The glossary also distinguishes:

- **Chain of Identity (COI):** evidence connecting material and product to the intended patient.
- **Chain of Custody (COC):** evidence showing who possessed, transferred or handled the material or product, where and when.

COC includes more than courier tracking. It includes all relevant custody transfers.

“Manufacturing complete” is not the same as “Quality released.”

### Bounded contexts and context map

A bounded context is a business area with its own responsibility and vocabulary. The model identifies 15 contexts, including Identity and Lineage, Capacity Planning, Quality Management and Journey Coordination.

Manufacturing owns execution evidence. Quality owns the release decision. Journey Coordination combines relevant evidence into a journey view but does not inherit Quality authority.

Anti-corruption adapters translate source formats while preserving source meaning. A source status such as `RELEASED` must not automatically become “Quality release approved.”

### Ownership and authority

This artifact answers: “Who is allowed to establish this fact or decision?”

Manufacturing may establish manufacturing progress. An authorised Quality decision establishes product release. Conflicting identifiers remain visible and move into an authorised resolution process.

### Business rules and decision tables

Rules connect evidence to permitted outcomes. They distinguish `SATISFIED`, `NOT_SATISFIED`, `UNKNOWN` and `NOT_APPLICABLE`.

For safety-critical prerequisites, `UNKNOWN` blocks progression. The system investigates; it does not guess.

Timeouts are also controlled. If a reservation request times out, the outcome becomes `OUTCOME_UNKNOWN` and the system reconciles before retrying. This prevents duplicate bookings.

### Domain events and time

A command requests a side effect. A domain event records that a relevant fact or decision happened.

The model preserves:

- `occurred_at`: when the business event happened.
- `recorded_at`: when the platform learned or stored it.

Corrections add new evidence instead of erasing history. This supports auditability and replay.

### State machines

The executable model covers four lifecycles:

1. Therapy journey
2. Identity case
3. Command saga
4. Quality release

A guard is a condition that must be satisfied before a state change. An AI recommendation cannot directly trigger a consequential state transition.

The specification records 11 rules, 53 event types, four state machines and 52 transitions. The validator and five focused tests passed. One missing `AuthorizationDenied` event was caught and corrected, demonstrating that the validator can detect catalogue drift. This is internal consistency evidence, not proof of complete safety.

**Stage 5 output:** shared vocabulary, ownership, rules, events and permitted state changes.

## Stage 6 — Qualify data and knowledge

Stage 6 checks whether the evidence required by Stage 5 exists, can be trusted and may be used.

### Inventory

The measured inventory includes 23 CSV datasets with 27,507 rows, 800 synthetic patient records represented across relevant exports, 6,407 events across eight event types, 60 shadow email files, spreadsheets, SOPs and supporting documents.

### Data-quality findings

The issue register contains 14 categories, including duplicate MRN groups, DOB disagreements, MES/QMS release conflicts and shipment sequences where arrival appears before departure.

These findings become requirements and test cases. They do not automatically identify which source is correct.

### Lineage, provenance and trust

Lineage shows how records and transformations connect. Provenance shows where a particular piece of evidence came from. Source trust asks whether that source can support this particular fact or decision.

The SQLite database copies corresponding CSV data, so matching values are not independent confirmation.

### Permissible use

The academic boundary is synthetic data for local work, minimum-necessary access and external AI denied by default. Availability does not equal permission.

### Data gaps and controlled knowledge

The gap register makes missing evidence and policy visible. Examples include identity-resolution rules, custody evidence, assay specifications and blocking-deviation rules.

The SOP register distinguishes effective, draft and superseded documents. Draft and superseded procedures cannot authorise current execution.

### Fitness conclusion

| Use | Conclusion |
|---|---|
| Brownfield investigation | Fit |
| Deterministic POC | Fit with explicit gaps |
| Synthetic AI evaluation | Conditional on rubrics and controls |
| Real identity resolution or product disposition | Not fit |
| Production performance or compliance claims | Not supported |

**Stage 6 output:** evidence inventory, quality findings, trust boundaries, permissible-use rules and visible gaps.

## Stage 7 — Define evaluations, impacts and risks

Stage 7 defines the exam before building the answer.

### Comparison arms

- **Arm A:** supplied/manual baseline.
- **Arm B:** deterministic rules and human workflow with AI disabled.
- **Arm C:** Arm B plus bounded AI assistance.

This separates the value of the core workflow from any additional AI value.

### Scenario catalogue

There are 57 specified cases: six supplied seeds, ten failure injections and 41 extensions. They cover identity conflicts, withdrawn consent, QMS outages, duplicate retries, misleading notes, provider failure and other boundary conditions.

They are marked `SPECIFIED_NOT_RUN`. The tests are defined; the future system has not passed them.

### Impact, risks and oversight

AI is limited to extracting, summarising, explaining and recommending. It cannot approve identity, release product or make a clinical decision.

The harm register contains 17 scenarios with controls and owners. Human oversight requires evidence inspection and the ability to reject, abstain or escalate.

Stage 7 defines adversarial cases for later AI red teaming. Execution belongs to Stage 15.

**Stage 7 output:** evaluation strategy, thresholds, scenarios, impact assessment, harm treatments and oversight requirements.

## Stage 8 — Select the solution

Stage 8 compares options using consulting, product, architecture and commercial judgement.

The six options are patching the prototype, a rules-only modular monolith, a modular core plus one optional assistant, multi-agent orchestration, SaaS or partner purchase, and a distributed rebuild.

Safety and authority receive the largest trade-off weight at 25 percent.

Option 3 scores 4.70 out of five. Option 2 scores 4.58 and remains the mandatory fallback. These are decision scores, not measured business benefits.

Eight focused technical tests passed. They cover duplicate-command handling, unknown outcomes, Quality authority and AI-off fallback. They support feasibility, not production reliability.

Preliminary ADRs record the modular monolith, durable command ledger, provider-neutral AI and no AI decision authority.

The build-versus-buy and TCO analysis includes integration, operations, model usage and human review. Missing prices remain unknown.

Gate 2 approved the direction for academic design and build. The deterministic workflow is the default. If AI is unavailable, unsafe, too expensive or unable to demonstrate additional value, the workflow continues without it.

**Stage 8 output:** selected solution, trade-offs, technical-spike evidence, preliminary ADRs and academic Gate 2 decision.

## The complete connection

**Stage 5:** What do the terms, rules and authorities mean?

**Stage 6:** Can the evidence support those rules?

**Stage 7:** How will we judge success, failure and AI value?

**Stage 8:** Which solution best fits the evidence, controls and evaluation requirements?

The answer is a deterministic core with an optional bounded AI assistant. The assistant must earn its place through evidence, while authorised people retain consequential decisions.
