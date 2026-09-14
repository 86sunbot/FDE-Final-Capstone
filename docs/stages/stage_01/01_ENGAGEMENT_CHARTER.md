# Stage 1 - Engagement Charter

**Programme:** CGT Patient-to-Batch Orchestration Capstone  
**Lifecycle:** 21-stage AI FDE Operating Model  
**Delivery approach:** Spec-driven development using Codex  
**Artifact status:** Ready for stakeholder review  
**Last updated:** 2026-09-14

## 1. Mandate

Assess a deliberately imperfect, synthetic multinational Cell and Gene Therapy patient-to-batch estate and deliver an evidence-driven, locally runnable proof of concept that demonstrates how deterministic engineering and bounded AI assistance can reduce patient-at-risk conditions, manual coordination and avoidable delay.

The work must discover and prove the actual problems before selecting or building solutions.

## 2. Context

The simulated estate coordinates an autologous therapy journey across patient onboarding, eligibility and consent, apheresis, Chain of Identity and Chain of Custody, cryogenic logistics, manufacturing capacity, manufacturing execution, QC testing, QA release, return logistics, conditioning and infusion readiness.

Information is distributed across CRM, clinical, scheduling, ERP, MES, LIMS, QMS, courier and shadow-operation surfaces. Contradictions are deliberate challenge evidence and must not be globally “cleaned up” without an approved requirement.

All data, people, organizations and events are synthetic. This capstone is not a clinical, medical, validated GxP or production system.

## 3. Problem statement

The estate lacks a consistently trustworthy and auditable patient-to-product operational view. Fragmented identifiers, inconsistent state meanings, weak temporal semantics, duplicated rules, partial transactions, manual workarounds and unclear decision authority can create unsafe readiness conclusions, duplicate capacity actions, delayed exception response and weak assurance.

The capstone must determine:

1. Which problems are proven by evidence.
2. Which problems require deterministic engineering.
3. Where AI assistance has a justified advantage.
4. Which actions must remain human-authorized.
5. What evidence is required before recommending a controlled pilot.

## 4. Intended outcomes

1. Reproducible brownfield forensic assessment.
2. Reconstructed domain, current journey and decision model.
3. Prioritized problem statement and measurable KPI baseline.
4. Functional, non-functional and assurance requirements.
5. Target architecture, ADRs and reversible migration strategy.
6. Three integrated workflow POCs.
7. TEVV covering normal, edge, adversarial, outage, recovery and authority cases.
8. Security, privacy, Responsible AI and governance analysis.
9. Resilience, recovery and operational-handover package.
10. Honest production-readiness gap assessment and 90-day roadmap.

## 5. Planned workflow proofs

### POC 1 - Patient and identity readiness

Reconcile identity evidence without fabricating a match; check consent, authorization, site qualification and Chain of Identity; enforce legal state transitions; route uncertainty to an authorized human.

### POC 2 - Manufacturing disruption and slot orchestration

Demonstrate persistent idempotency, capacity conflicts, disruption impact, alternatives, compensation/rollback, evidence-backed recommendations and authorized execution.

### POC 3 - Product, QA and thermal-release support

Separate manufacturing completion from QA release; account for QC and blocking deviations; analyze controlled thermal evidence; preserve Quality disposition authority; prevent premature downstream readiness.

## 6. In scope

- All evidence contained in the immutable challenge ZIP.
- Current-state and target-state process, information, application, AI and operational design.
- Local-first implementation and tests.
- Optional model adapter disabled by default.
- Deterministic safety gates and explicit state machines.
- Evidence, provenance, confidence, authority and audit metadata.
- Three integrated POCs operating on verified working copies of synthetic data.
- Internal assurance and evidence preparation for later independent review.
- Shadow/canary simulation and a conditional pilot recommendation.

## 7. Out of scope

- Real patient, clinical or production data.
- Autonomous clinical, identity, Chain of Identity, Chain of Custody, Quality-release or product-disposition decisions.
- Unapproved mutation or “repair” of the challenge evidence.
- Real MES, QMS, LIMS, ERP, courier or hospital production integrations.
- Claims of validated GxP status, regulatory compliance, production deployment or external audit.
- Big-bang replacement of the simulated brownfield estate.
- Claimed savings or KPI improvement without an explicit measurement basis.
- Retirement of any real enterprise system.

## 8. Non-negotiable constraints

- Preserve the original ZIP byte-for-byte.
- Do not nominate a global source of truth without evidence.
- Represent unresolved identity and lineage uncertainty explicitly.
- Record event time separately from recorded/ingested time.
- Treat units and identifiers as typed data.
- Use idempotency and payload-conflict detection for commands.
- Add tests before repairing intentional defects.
- Prefer reversible, incremental migration.
- Keep the baseline runnable without cloud credentials.
- Treat all AI output as untrusted recommendation data.
- Require authenticated human authority for consequential mutations.

## 9. Delivery method

Each stage follows:

`SPECIFY -> BUILD -> VERIFY -> SHIP -> REPEAT`

Each consequential feature maintains:

`Evidence -> Lens/root cause -> Requirement -> ADR -> Code -> Test/eval -> KPI -> Lifecycle decision`

Stage status is evidence-based. Artifact existence alone does not establish completion.

## 10. Measures of capstone success

- A clean clone or clean local package reproduces the forensic findings.
- All evidence sources, assumptions and transformations are traceable.
- One canonical domain vocabulary and state model are used across APIs, code and tests.
- The three POCs run through shared services rather than duplicate workflow logic.
- All P0 safety requirements have negative and failure-mode tests.
- Missing or uncertain safety data fails closed.
- Consequential decisions prove authenticated human authorization.
- Original evaluation cases and failure injections execute against the integrated system.
- Measured results are separated from targets and hypotheses.
- Residual risk and production gaps remain visible.

## 11. Governance and approval

Codex is responsible for evidence analysis, drafting, implementation, testing and maintaining traceability. Codex is not accountable for clinical, Quality, regulatory, security, privacy or lifecycle approval.

Until named stakeholders are confirmed, role-based owners in the RACI are proposed placeholders. Stage 1 may be internally ready for review but cannot be marked approved by Codex.

## 12. Stage 1 decision requested

The Capstone Owner should confirm or amend:

1. Mandate and scope.
2. Intended audience and assessment criteria.
3. Role-based governance and decision rights.
4. Eight-week working sequence or required deadline.
5. Final presentation and demonstration expectations.

Approval record: **Pending**.
