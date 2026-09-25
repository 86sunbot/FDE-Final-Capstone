# FDE Capstone — 10-Minute Presentation Talk Track

**Slides covered:** Stage 05 — Executable Domain Model; Stage 06 — Evidence Baseline & Gaps; Stage 07 — Define the Exam Before the Answer; Stage 08 — Works With AI. Works Without It.

> **Presenter note:** Everything below each slide title is intended to be spoken. Bold text is a speaking anchor—give it slight emphasis or use it to recover your place. Do not read every number or heading on the slide.

---

## Slide 1 — Executable Domain Model | ~2.5 min

“Before we talk about architecture or AI, there is a more fundamental question: **what must actually be true in the physical world before the system makes an operational decision?**

That is what we tried to answer through this domain model.

We identified **15 patient-specific domains** and represented what happens across them through events, rules, transitions and state machines.

But the numbers aren't really the important part here. The important part is that we converted **business reality into explicit rules the system can enforce**.

For example, **COI is not the same as COC**. An API status is not automatically trusted. And MES saying ‘complete’ does **not** mean the drug is released.

We also had to define what happens when reality isn't clean.

If identifiers conflict, we don't silently merge them. We create an **owned case**. If evidence is unknown, the affected safety-critical step is **blocked**, while the investigation can continue.

And this led to an important architecture principle: **state changes require valid evidence, a legal transition and the right authority.**

AI can recommend, but **AI cannot directly change the domain state**.

So once we had defined what truth should look like, our next question was: **does the data we actually have support that truth?**”

---

## Slide 2 — Evidence Baseline & Gaps | ~2.5 min

“And that's what we looked at next.

Because defining the domain is one thing. But if the underlying evidence is incomplete or contradictory, **the system cannot safely act on it**.

So instead of assuming the data was ready, we tested it.

We looked at more than **27,000 primary records**, around **6,400 events**, across a synthetic population of **800 patients**.

But one of the interesting findings wasn't inside the formal systems at all.

We found **60 shadow emails** capturing operational workarounds.

And that tells us something important: **the real business process is larger than the applications that supposedly support it.**

Once we started checking the quality and provenance of the evidence, more gaps appeared.

We found MES and QMS release conflicts, date-of-birth disagreements, duplicate MRNs, schedule clashes and missing reasons.

And **188 out of 188 provenance links were unresolved**.

We didn't try to hide those gaps or clean them away just to make the POC work. We treated them as **part of the problem the architecture has to handle**.

We also looked at governance.

Having an SOP doesn't automatically mean it is authoritative. One version here was **active and binding**, while another was still a **draft**.

So the question isn't simply, ‘Do we have data?’

It's **‘Do we have evidence we are allowed to trust for this particular decision?’**

And because this is an academic POC, we also kept the boundary very clear: **synthetic data only, no production PII or PHI, and external cloud LLM calls are denied by default.**

At this point, we understood the domain and we understood the limitations of our evidence.

But before choosing an architecture, we wanted to answer another question:

**What would a good solution actually have to prove?**”

---

## Slide 3 — Define the Exam Before the Answer | ~2.5 min

“This became one of the principles I liked most in the project:

**define the exam before the answer.**

Instead of building something first and then designing tests that it could pass, we reversed that.

We defined **57 test scenarios** covering normal behaviour, boundary conditions, faults and adversarial situations.

We also identified **17 potential harms**, and designed the evaluation across **eight TEVV layers**.

But there is an important point here.

Not everything can simply become a weighted score.

For example, we defined a P0 requirement of **zero unauthorized consequential actions**.

If the system violates authority, it doesn't matter that it performed well on ten other criteria.

**Safety failure overrides the score.**

The same thinking applies to auditability.

For consequential decisions, we require **100% audit coverage**—who acted, when, based on what source, and how that action can be correlated back to the evidence.

And AI creates another interesting testing problem.

We shouldn't only test whether AI gives us the correct answer.

We also test what happens when AI gives us a **very convincing wrong answer**.

Will the surrounding system blindly accept it?

Or will the deterministic controls stop it?

That distinction is important because we're not trying to prove that an LLM is always right. We're trying to prove that **the system remains safe when it isn't**.

And you'll notice this evaluation doesn't end at this slide.

We define the tests here, later stages build and execute them, and eventually the appropriate authority accepts the **residual risk**.

So now we have three things: we understand the domain, we understand the evidence, and we've defined what success and failure mean.

**Only now are we ready to choose the architecture.**”

---

## Slide 4 — Works With AI. Works Without It. | ~2.5 min

“And this is where those earlier decisions start coming together.

We evaluated several possible architectures against **12 criteria**, including safety and authority.

We looked at patching the legacy system, multi-agent approaches, SaaS, microservices and other options.

But we deliberately did **not** start with the assumption that because this is an AI project, AI has to run the system.

The architecture we selected has a **deterministic core**.

That core owns the things we cannot afford to make probabilistic: the immutable baseline, the command ledger, authority and the safety-critical rules.

Then we place a **bounded AI assistant** above it.

AI can help interpret information. It can assist the user. It can make recommendations.

But it has **no consequential command authority**.

And there's a very simple test for whether we've separated those responsibilities correctly:

**What happens if AI disappears tomorrow?**

The answer should be: the core business process **continues to work**.

If the model is unavailable, if the provider changes, or if AI fails our safety, cost or value tests, we can disable that layer and **fall back to the deterministic core**.

So an AI outage does not automatically become a business-process outage.

And that brings me back to the overall FDE journey across these four slides.

We didn't start by asking, **‘Where can we put AI?’**

We started by asking, **‘What is true?’**

Then, **‘Can our evidence prove it?’**

Then, **‘How will we test whether the solution is safe?’**

And finally, **‘What architecture survives those constraints?’**

That's the FDE capability I wanted this work to demonstrate:

**understand the domain, challenge the evidence, define how success will be proven, and only then build the technology around it.**

AI is part of the solution.

**It is not the foundation of trust.**”


---

## Stage 12 — Safety Boundaries for a Connected Journey | ~2.5 min

“Now that we have the architecture, the next question is: **what stops a source note, a user request, or an AI suggestion from becoming an unauthorized action?**

We started with the **threat model**.

We used the OWASP LLM and Agentic risk categories as **threat prompts**, and mapped scenarios such as **role spoofing, cross-patient access, prompt injection, tool misuse, replay and audit tampering**.

For example, what if a source note contains instructions telling the AI to bypass a release rule? Or what if an AI confidently recommends a Quality decision without sufficient evidence?

Our answer is not to trust the AI to behave correctly. We enforce the boundary **outside the AI**.

That's the second part of the slide — **server and human controls**.

The server validates **authentication, role, scope, state and evidence** before a consequential action. We also enforce input validation, idempotency and auditability at that deterministic layer.

The assistant operates with **least privilege**. It can read and recommend, but it has **no mutating or release tools**.

So even if we get a persuasive but incorrect AI response, it cannot simply turn that response into a shipment, batch or Quality action.

And **named human roles retain approval authority** for consequential decisions.

We also considered **privacy and data protection**. In this POC, we're using synthetic data, scoped fields, and **no external AI provider**. We deliberately avoid sending an entire repository or unrestricted patient context into a prompt.

For auditability, actions are captured in an **append-only logical ledger with a hash chain**. Again, that's the POC implementation — production would require controls such as validated immutable storage, enterprise identity, encryption, DLP and formal retention.

The third area is **supplier and exit risk**.

We maintain **SBOM and AIBOM** records, there is no dynamic tool registry, and no live AI provider has been selected.

And importantly, AI is **off by default**.

If AI becomes unavailable, unsafe, or simply doesn't add enough value, we can turn it off and **the deterministic workflow still operates**.

That's what the diagram on the right is showing.

**Source systems provide claims. AI provides suggestions. Humans provide approval. The server enforces the guards.**

And there is an important limitation here.

This is an **internal security design mapping for a synthetic academic POC**. It is not an OWASP certification, penetration test, or proof that live LLM security has passed.

In fact, because we deliberately use off and fake modes today, **live-model red teaming, production IAM, DLP, supplier assurance and penetration testing remain production gates**.

So the security principle behind this stage is very simple:

**external content carries no authority, AI carries no authority, authorized people decide, and deterministic server controls enforce the decision.**”

### Evidence / artifacts — not spoken

- `docs/stages/stage_12/01_THREAT_MODEL.md` — security threat model.
- `docs/stages/stage_12/02_SECURITY_PRIVACY_AND_GUARDRAIL_CONTROLS.md` — authentication, authorization, least privilege, data minimization, audit, input/output guardrails, DLP, availability and secure-delivery mapping.
- `docs/stages/stage_12/03_SUPPLIER_SBOM_AIBOM_AND_EXIT_PLAN.md` — supplier controls, SBOM/AIBOM and AI exit strategy.
- `docs/stages/stage_12/05_OWASP_2026_RISK_MAPPING.md` — OWASP LLM/Agentic risk-family mapping used as threat prompts; not a certification.
- `docs/stages/stage_12/06_ACADEMIC_AI_SYSTEM_CARD.md` — academic system boundary and limitations.
- `docs/stages/stage_07/04_RISK_HARMS_AND_TREATMENT_REGISTER.md` — upstream risk evidence covering unauthorized actions, prompt injection, disclosure, hallucination, outage, audit integrity and human over-reliance.

> **Evidence boundary:** Stage 12 is an internal design mapping for the local synthetic demonstrator. Live-model red teaming, enterprise IAM/DLP, supplier assurance, immutable production audit storage and penetration testing remain production gates.
