# 5-Minute Executive UI Demo Guide
## "The Orchestrated Journey of Patient P-A (and the P-00013 Safety Catch)"

This guide provides a crisp, minute-by-minute walkthrough script for demonstrating the **CGT Control Tower** to an executive, clinical, or engineering audience in exactly 5 minutes using a single cohesive patient narrative.

---

### Quick Setup
1. **Ensure the Control Tower server is running**:
   - Double-click `START_DEMO.command` in macOS Finder, or run in terminal:
     ```bash
     FDE_DB=runtime/control-tower.db AI_MODE=off PYTHONPATH=src \
       .venv/bin/python -m uvicorn fde_capstone.api:app --host 127.0.0.1 --port 8000
     ```
2. **Open browser**: Navigate to <http://127.0.0.1:8000>.
3. **Set Assistant Mode**: Leave as **`AI off · recommended`** (default).

---

### Timing Breakdown

```
[00:00 - 01:00]  ACT 1: The Fatal Trap (Patient Dashboard & P-00013)
[01:00 - 02:00]  ACT 2: Gate 1 — Identity & Clinical Readiness (POC 1)
[02:00 - 03:00]  ACT 3: Gate 2 — Manufacturing Slot Allocation (POC 2)
[03:00 - 04:00]  ACT 4: Gate 3 — Formal QA Batch Release (POC 3)
[04:00 - 05:00]  ACT 5: The Mathematical Proof — Audit Chain & Executive Wrap
```

---

### Minute-by-Minute Choreography & Word-for-Word Script

#### [00:00 – 01:00] ACT 1: The Fatal Trap (Why Status Labels Lie)
* **Where to look**: Click **Patient Dashboard** in the top navigation bar (`#dashboard`).
* **Action**:
  1. Point to the KPI banner: **800 Total Patients**, **673 Active**, **25 Infusion Ready**, **14 QA Holds**.
  2. Click the red **QA Hold** filter pill, or type `P-00013` into the search box.
  3. Click on row **`P-00013`** to expand its drawer.
* **What to say**:
  > *"Team, in autologous cell therapy, every batch is manufactured from a single living patient's cells. One batch costs upwards of $450,000 and has zero shelf life. 
  > Look at patient **P-00013**. In the inherited legacy system, this patient was prematurely labeled 'INFUSION READY'. A clinic acting on that status would have scheduled patient infusion.
  > But look at what our Control Tower did: it caught an open manufacturing hold flag in the raw batch records. Our engine overrode the label, set governing status to **`BLOCKED_QA_HOLD`**, and strictly flagged infusion authorization as **`PROHIBITED`**. 
  > In this system, **status labels never create truth; only verified evidence does.**"*

---

#### [01:00 – 02:00] ACT 2: Gate 1 — Resolving Identity Without Guessing (POC 1)
* **Where to look**: Scroll back up to the **Hero section** or down to **`#pocs`**.
* **Action**: Click the blue button: **`▶ Run end-to-end demo`**.
* **What happens on screen**: 
  - The 8-stage progress tracker animates across *Enrollment → Identity → Authorization → Slot → Manufacturing → QC → Quality Release → Ready*.
  - **`POC 01: Identity & readiness`** card turns green with badge **`APPLIED · SATISFIED`**.
* **What to say**:
  > *"Now watch what happens when we orchestrate an active patient—**Journey P-A / BATCH-100**.
  > At Gate 1, the apheresis clinic and downstream lab submitted conflicting birth dates and medical record numbers. 
  > A brittle pipeline either crashes or guesses. Our orchestrator did neither: it created an **owned identity case**, halted automated progression, and required a simulated human Identity Authority to sign off. Only with explicit human authorization did readiness transition to **`SATISFIED`** with immutable audit citations."*

---

#### [02:00 – 03:00] ACT 3: Gate 2 — Manufacturing Slot Locking & Idempotent Safety (POC 2)
* **Where to look**: Look at the second card: **`POC 02: Slot allocation & idempotency`**.
* **What happens on screen**:
  - Shows status: **`SUCCEEDED`**, **`DISPATCH: 1`**, **`CONFLICTS: 0`**.
* **What to say**:
  > *"Next, we must book an expensive cleanroom manufacturing slot across manufacturing sites. 
  > During this live call, the external reservation API actually timed out. In typical microservices, a blind retry would have dispatched a duplicate request and double-booked a scarce cleanroom suite.
  > Here, the orchestrator marked the initial outcome as **`UNKNOWN`**, safely queried the external system state, reconciled that the slot was indeed reserved, and completed the step without a duplicate reservation. It guarantees **exactly-once execution**."*

---

#### [03:00 – 04:00] ACT 4: Gate 3 — Formal QA Batch Release (POC 3)
* **Where to look**: Look at the third card: **`POC 03: Quality release & CoA`**.
* **What happens on screen**:
  - Shows status: **`SATISFIED`** with verified Certificate of Analysis (CoA) reference.
* **What to say**:
  > *"Now the therapy is manufactured, QC lab tests pass, and cryogenic transit temperatures are green.
  > Even with perfect data, **software is legally prohibited from releasing a living drug**. 
  > Notice that release status remained strictly `UNKNOWN` until the authorized Quality Authority executed a formal digital release disposition. Only after human QA sign-off did the batch become **`RELEASED`** and patient P-A become **`INFUSION READY`**."*

---

#### [04:00 – 05:00] ACT 5: The Mathematical Proof — Tamper-Evident Audit Chain & Summary
* **Where to look**: 
  1. Look at the **Automated Cross-Domain Summary** box (under `#roles`).
  2. Point to the top right of the Hero panel: **`Tamper-evident audit chain active`** displaying the live **SHA-256 hash**.
* **Action**:
  - In the **Demonstrate as** dropdown, switch from *Patient Operations* to **Quality Authority** or **Executive / Operations Viewer**.
* **What to say**:
  > *"To close: notice this isn't just UI smoke and mirrors. 
  > Every single event—the identity resolution, the slot reconciliation, and the QA signature—was appended to an in-memory **SHA-256 cryptographic audit chain** (pointing to the hash on screen). If any record is tampered with, the chain breaks.
  > Notice also that **AI is turned off by default**. Every decision on this screen is 100% deterministic and rule-governed. AI can explain what happened, but it is never permitted to make clinical or GxP decisions.
  > 
  > **Summary for the team:** We have turned fragmented spreadsheets and siloed APIs into a single, evidence-backed control tower that protects patient safety at every step."*

---

### High-Stakes Q&A Responses

* **Q: "Why do we keep AI off if this is an AI FDE Capstone?"**
  > **Answer:** *"Under 21 CFR Part 11 and GxP, non-deterministic AI cannot authorize patient release or resolve identities. We use deterministic state machines for authoritative control, reserving AI strictly as an optional, read-only explanation assistant."*

* **Q: "Is this connected to our real hospital systems yet?"**
  > **Answer:** *"No. This is a fully functional synthetic demonstration running against 800 synthetic patient records. Our final lifecycle decision is **'Restrict and Change'**: we must remediate 7 registered CAPAs before piloting with live data."*
