# 12-minute talk track: Stages 5–8

## 0:00–1:00 — Connect to Stages 1–4

“Our capstone coordinates a patient-specific therapy journey in Cell and Gene Therapy, or CGT. Cells are collected from a patient, transported for manufacturing, processed, tested and returned for treatment after the required approvals.

Stage 1 established the mandate, stakeholders and responsibilities. Stage 2 examined the existing process and systems through process discovery and brownfield assessment. Stage 3 framed the problem, investigated root causes and identified baseline KPIs and evidence gaps. Stage 4 assessed AI suitability, the conventional-automation alternative and the academic boundaries.

Stages 5 to 8 take us from understanding the problem to selecting a solution we can build and evaluate.”

## 1:00–4:00 — Stage 5: Model the domain

“Stage 5 gives everyone a shared understanding of the business. This is Domain Modelling using Domain-Driven Design, or DDD.

We started with the domain glossary. A patient is the person receiving therapy. A collection is the starting material collected from that patient. A shipment moves the material or manufactured product. A manufacturing batch is the patient-specific unit of manufacturing work. Quality release is the authorised decision that the required release conditions have been met.

These definitions matter because completing one step does not automatically permit the next step. Manufacturing may be complete while quality testing or release approval is still pending.

The glossary separates Chain of Identity from Chain of Custody. Chain of Identity provides evidence that material and product belong to the intended patient. Chain of Custody records who possessed or handled them, where and when.

The bounded-context map divides the domain into 15 areas with clear responsibilities, including identity, manufacturing, quality and scheduling. These are business boundaries; they do not require 15 separate applications. Adapters translate information from existing systems while preserving the original source meaning.

The authority matrix defines who may establish each fact or decision. Manufacturing can establish manufacturing progress. An authorised Quality decision establishes product release. Conflicting patient identifiers are preserved and routed to an authorised resolution process.

The business rules use fail-closed behaviour. If safety-critical evidence is missing or unknown, the affected action stops. For example, a temperature event can create a Quality investigation, but it cannot automatically approve or reject the product.

Domain events record what happened and preserve when it happened and when the platform learned about it. The state machines define permitted status changes. An AI recommendation cannot directly move a product into a released state.

The executable specification records 11 rules, 53 event types, four state machines and 52 transitions. Five focused domain tests passed. These are internal consistency checks; domain-owner validation remains separate.

Stage 5 gives us shared terms, ownership, rules and permitted transitions. It also gives later API and event-contract engineering a stable business foundation.”

Transition: “Now that we know what truth means, can the available evidence support it?”

## 4:00–6:20 — Stage 6: Qualify data and knowledge

“Stage 6 examines the evidence available to the project.

The inventory records 23 CSV datasets with 27,507 rows, records representing 800 synthetic patients, more than 6,400 events and 60 shadow email files, alongside spreadsheet exports.

The data-quality profile identifies 14 issue categories. Examples include conflicting patient details, disagreements between manufacturing and Quality release statuses, and shipment records where arrival appears before departure.

This supports the Stage 5 rule that manufacturing completion does not establish Quality release.

Lineage and provenance record where evidence came from and how it was copied or transformed. The SQLite database copied raw CSV information, so matching values there are not two independent confirmations.

The permissible-use register establishes the academic boundary: synthetic data for local work, minimum necessary access and external AI denied by default.

The data-gap register makes missing policies and evidence visible. Examples include identity-resolution policy, custody evidence, assay specifications and blocking-deviation rules. Each gap must be obtained, explicitly simulated, designed as UNKNOWN or removed from scope.

The SOP register distinguishes effective, draft and superseded documents. A draft procedure cannot authorise a workflow, and a superseded version cannot govern a current decision.

The fitness conclusion is deliberately limited. The evidence is fit for inherited-system investigation and a deterministic proof of concept with explicit gaps. It is conditionally fit for synthetic AI evaluation. It is not fit for real identity resolution, product disposition, production performance or compliance claims.

Stage 6 therefore covers data quality, lineage, provenance and knowledge discovery. It qualifies the evidence; later stages design the target data and semantic architecture.”

Transition: “We now have a domain model and an evidence assessment. Next we define how a future solution will be judged.”

## 6:20–9:00 — Stage 7: Define evaluations, impacts and risks

“Stage 7 defines how success and failure will be measured before the solution is built. This is Evaluation and TEVV: testing, evaluation, verification and validation.

There are three comparison arms. Arm A represents the supplied manual baseline. Arm B uses deterministic rules and human workflows with AI disabled. Arm C adds bounded AI assistance to Arm B. This separates improvement from the core solution from any additional AI value.

The scenario catalogue contains 57 cases: six supplied seeds, ten failure injections and 41 extensions. They cover normal journeys, boundary conditions, failures and adversarial inputs. They are currently specified but not run. That means the tests are defined; it does not mean the future system has passed them.

P0 thresholds require zero unauthorised consequential actions, zero invented identity relationships, zero illegal state changes, zero duplicate external effects and complete audit evidence.

The AI impact assessment limits AI to extracting, summarising, explaining and recommending. AI cannot approve identity, release product or make a clinical decision.

The harms register describes 17 potential harm scenarios, their controls and accountable roles. The human-oversight protocol requires the reviewer to inspect evidence and be able to reject, abstain or escalate. A fluent AI response must not replace authorised review.

The catalogue includes adversarial cases, but Stage 7 does not claim that full AI red teaming has been completed. Stage 7 specifies the cases; Stage 15 executes red teaming and independent assurance.

Stage 7 gives us the acceptance conditions and evidence plan needed to compare solution options fairly.”

Transition: “With the exam defined in advance, we can compare options without moving the goalposts.”

## 9:00–11:30 — Stage 8: Generate, test and select options

“Stage 8 applies consulting, product, architecture and commercial judgement.

The solution catalogue compares six options: patch the inherited prototype, build a rules-only modular monolith, add one optional bounded assistant, use multi-agent orchestration, buy or partner for a SaaS platform, or undertake a distributed rebuild.

Safety and authority carry the largest weighting at 25 percent. A high overall score cannot rescue an option that fails a safety condition.

Option 3—the deterministic core with one optional assistant—scores 4.70 out of five. Option 2—the rules-only core—scores 4.58 and remains the required fallback. These are decision scores based on stated criteria, not measured business benefits.

Eight focused technical tests passed. They examined duplicate-command handling, uncertain outcomes, Quality authority and fallback when AI fails. They support feasibility but do not prove complete production reliability.

The preliminary ADRs record the choices and their reasons: modular monolith first, a durable command ledger, provider-neutral AI and no AI decision authority.

The build-versus-buy assessment, provider comparison and Total Cost of Ownership model include integration, operations, model usage and human review. Missing prices remain unknown.

Gate 2 approved the direction for academic design and build. Rules-only behaviour remains mandatory and is the default. If AI is unavailable, unsafe, too expensive or unable to demonstrate additional value, the deterministic workflow continues without it.

This is an approved academic solution direction, not production approval.”

## 11:30–12:00 — Handover to Design

“Stage 5 defined business terms, rules and authority. Stage 6 assessed the evidence and exposed its gaps. Stage 7 defined the tests and acceptance conditions. Stage 8 selected a solution with a rules-based core and optional AI assistance.

The Design stages can now turn these decisions into detailed contracts, architecture and controls. AI must earn its place through evidence, while authorised people retain consequential decisions.”
