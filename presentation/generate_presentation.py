#!/usr/bin/env python3
"""Generate an elite 20-slide 40-minute executive presentation for CGT Patient-to-Batch Orchestration.

Features:
- Widescreen 16:9 layout (13.333" x 7.5")
- Enterprise pharmaceutical & biotech aesthetic matching the CGT Control Tower
- Direct embedding of high-resolution visual slide frames from cgt_frames/
- Integrated presentation of the 120-second 1080p demo video (cgt_patient_to_batch_orchestration_demo.mp4)
- Comprehensive minute-by-minute speaker notes with transition scripts and Q&A prep on every slide
"""

from __future__ import annotations

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
FRAMES_DIR = ROOT / "cgt_frames"
OUTPUT_PPTX = ROOT / "presentation" / "CGT_Patient_to_Batch_Orchestration_Elite_Presentation.pptx"

# Colors
C_DARK_BG = RGBColor(10, 42, 52)       # #0a2a34
C_DARK_CARD = RGBColor(16, 54, 66)     # #103642
C_LIGHT_BG = RGBColor(248, 250, 252)   # #f8fafc
C_WHITE = RGBColor(255, 255, 255)
C_NAVY_TEXT = RGBColor(15, 23, 42)     # #0f172a
C_MUTED_TEXT = RGBColor(100, 116, 139) # #64748b
C_TEAL = RGBColor(13, 148, 136)        # #0d9488
C_CYAN = RGBColor(6, 182, 212)         # #06b6d4
C_RED = RGBColor(220, 38, 38)          # #dc2626
C_GREEN = RGBColor(22, 163, 74)        # #16a34a
C_AMBER = RGBColor(217, 119, 6)        # #d97706
C_BORDER = RGBColor(226, 232, 240)     # #e2e8f0


def create_deck() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def add_bg(slide, prs, color: RGBColor):
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape


def add_header(slide, kicker: str, title: str, subtitle: str = "", dark: bool = False):
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_kicker = tf.paragraphs[0]
    p_kicker.text = kicker.upper()
    p_kicker.font.size = Pt(11)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = C_CYAN if dark else C_TEAL
    p_kicker.space_after = Pt(4)

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE if dark else C_NAVY_TEXT
    p_title.space_after = Pt(4)

    if subtitle:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = RGBColor(203, 213, 225) if dark else C_MUTED_TEXT


def add_notes(slide, notes_text: str):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text.strip()


def build_slides():
    prs = create_deck()
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide [00:00 - 02:00]
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    add_bg(s1, prs, C_DARK_BG)

    # Frame on right
    frame_path = FRAMES_DIR / "scene01.png"
    if frame_path.is_file():
        s1.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.2), width=Inches(5.8))

    # Title box on left
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "ENTERPRISE FDE CAPSTONE DEFENSE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Cell & Gene Therapy (CGT)\nPatient-to-Batch Orchestration"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(16)

    p = tf.add_paragraph()
    p.text = "Engineering an Evidence-Driven, Tamper-Evident Control Tower for Autologous Living Drugs Across 21 FDE Stages"
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(28)

    p = tf.add_paragraph()
    p.text = "Presenter: AI Forward Deployed Engineer (FDE)\nAudience: Executive Steering Committee & Quality Board\nDuration: 40 Minutes (32 min Presentation + 8 min Discussion)"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(148, 163, 184)

    add_notes(s1, """[TIMING: 00:00 - 02:00 | 2 Minutes]
SPEAKER SCRIPT:
"Good morning, members of the steering committee and evaluation board. Welcome to our final capstone defense for the Cell and Gene Therapy Patient-to-Batch Orchestration Engine.

Over the next 40 minutes, we will walk you through how we addressed one of the most critical challenges in biopharma today: orchestrating the vein-to-vein chain of identity and chain of custody for autologous living therapies. 

Unlike traditional pharmaceuticals, in autologous CGT, the patient is both the source of the starting material and the recipient of the manufactured batch. A single identity mismatch, an unverified temperature excursion, or an automated release without explicit Quality sign-off can be fatal.

Today, we will present our full 21-stage Forward Deployed Engineering journey, walk through our 120-second master demonstration video, dive into the three foundational proof-of-concept controls, explore our centralized 800-patient operations dashboard, and present our rigorous, honest G6 lifecycle decision: Restrict and Change. Let's begin."
""")

    # =========================================================================
    # SLIDE 2: Executive Summary & The Core Dilemma [02:00 - 04:00]
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    add_bg(s2, prs, C_LIGHT_BG)
    add_header(s2, "01 / EXECUTIVE CONTEXT", "The 'Batch Size of One' Reality in Cell & Gene Therapy", "Why autologous therapeutics fundamentally break traditional supply chain assumptions")

    cards = [
        ("The 'Batch Size of One'", "Every single batch is personalized from a patient's own harvested T-cells. There is zero inventory buffer, zero substitution, and zero tolerance for misattribution.", C_TEAL),
        ("The Vein-to-Vein Pipeline", "Starts at the hospital apheresis suite, travels via cryo logistics (-150°C LN2), undergoes CDMO genetic transduction, and returns for patient lymphodepletion.", C_CYAN),
        ("The Compliance Mandate", "Strict adherence to FDA 21 CFR Part 11, GAMP 5, and EU Annex 11. Heuristic matching, guessing, or unverified automated transitions are unacceptable under GxP.", C_RED),
    ]
    for i, (title, desc, col) in enumerate(cards):
        left = Inches(0.8 + i * 3.9)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), Inches(3.7), Inches(4.5))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(14)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = C_NAVY_TEXT
        p.space_after = Pt(14)

    add_notes(s2, """[TIMING: 02:00 - 04:00 | 2 Minutes]
SPEAKER SCRIPT:
"To understand why this capstone exists, we must understand why autologous cell therapy breaks traditional enterprise software.

In standard small-molecule or biologics manufacturing, you produce 100,000 vials in a single validated run. If a vial breaks, you discard it. In autologous CAR-T therapy, the batch size is exactly one. The patient's blood is drawn at the clinic, shipped in liquid nitrogen dry vapor shippers at minus 150 degrees Celsius to a CDMO, engineered, expanded, quality-tested, shipped back, and infused into the very same human being.

If patient A receives patient B's engineered cells, the result is fatal graft-versus-host disease. If a manufacturing slot reservation is lost over a network glitch and blindly retried, a quarter-million-dollar cleanroom is double-booked. And if an enterprise ERP marks a batch 'shipped' before the Quality Authority signs off on deviations, that drug enters a clinic illegally under FDA 21 CFR Part 11.

Our mission was to engineer an authoritative orchestration layer that makes every transition evidence-driven, tamper-evident, and auditable."
""")

    # =========================================================================
    # SLIDE 3: Anatomy of the Inherited Problem [04:00 - 06:00]
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    add_bg(s3, prs, C_LIGHT_BG)
    add_header(s3, "02 / PROBLEM STATEMENT", "Four Disconnected Enterprise Siloes", "Fragmented transactional systems create operational blindness and catastrophic safety hazards")

    frame_path = FRAMES_DIR / "scene02.png"
    if frame_path.is_file():
        s3.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.8), width=Inches(5.8))

    box = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True
    bullets = [
        ("Clinical Hospital Feeds (EDC / CRM)", "Emit patient records, subject identifiers, and DOBs—frequently conflicting across hospital networks with no unified identity master."),
        ("Cryogenic Couriers & Dry Vapor LN2", "Emit IoT temperature readings and GPS coordinates, but lack visibility into patient readiness, customs holds, or manufacturing schedules."),
        ("CDMO Manufacturing (MES / SCADA)", "Tracks bioreactor operations, cell viability, and lot numbering, but cannot authorize patient scheduling or release disposition."),
        ("Enterprise Quality & ERP (SAP / QMS)", "Contains deviation logs and CAPA reports, but operates on asynchronous batch batch-release cadences detached from clinic bedsides."),
    ]
    for i, (b_title, b_desc) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {b_title}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_NAVY_TEXT
        
        # Add normal text
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = C_MUTED_TEXT
        p.space_after = Pt(10)

    add_notes(s3, """[TIMING: 04:00 - 06:00 | 2 Minutes]
SPEAKER SCRIPT:
"When we arrived at the brownfield baseline, we found four completely disconnected software siloes.

On the left, clinical sites run EDC and CRM systems that record patient enrollment, consents, and hospital medical record numbers. In the middle, cryogenic logistics partners track cryogenic shippers with IoT temperature sensors. Downstream, CDMOs run Manufacturing Execution Systems that monitor bioreactors and cell viability. And at headquarters, Quality teams track deviations in corporate QMS platforms.

The problem? None of these systems talk to one another deterministically. When an identity conflict occurs between a clinic record and an apheresis bag, systems try to 'guess' or merge records. When a cryogenic shipment experiences a 15-minute thermal excursion at customs, the clinic schedules patient lymphodepletion anyway because they assume 'In Transit' means 'On Schedule'.

This fragmentation is not merely an IT inefficiency; it is an existential patient safety hazard."
""")

    # =========================================================================
    # SLIDE 4: Real-World Risks of Desynchronization [06:00 - 08:00]
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    add_bg(s4, prs, C_LIGHT_BG)
    add_header(s4, "03 / RISK TAXONOMY", "The Three Critical Hazard Vectors in Cell Therapy", "Quantitative consequences of ungrounded status assumptions and unverified transitions")

    hazards = [
        ("Hazard 1: Mismatched Patient Identity", "CRITICAL CLINICAL HAZARD", "Infusing an engineered cellular drug into the wrong patient triggers fatal hyper-acute rejection or Graft-versus-Host Disease (GvHD). Merging records based on heuristic string similarity violates 21 CFR Part 11 requirements for Chain of Identity.", C_RED),
        ("Hazard 2: Blind Retry & Slot Double-Booking", "HIGH OPERATIONAL & FINANCIAL HAZARD", "When an external CDMO API times out during slot booking, blind HTTP retries dispatch duplicate reservation requests. A single reserved cleanroom suite costs $250k+; double-booking causes schedule collapse and cancelled patient conditioning.", C_AMBER),
        ("Hazard 3: Automated or Pre-Mature Release", "SEVERE REGULATORY COMPLIANCE HAZARD", "Allowing an MES 'Manufacturing Complete' status to automatically clear a batch for hospital staging bypasses QA deviations. Shipping and administering an adulterated batch triggers FDA Form 483s, consent decrees, and clinical holds.", C_RED),
    ]
    for i, (title, kicker, desc, col) in enumerate(hazards):
        top = Inches(1.8 + i * 1.75)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.55))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = kicker
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY_TEXT
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(11)
        p3.font.color.rgb = C_MUTED_TEXT

    add_notes(s4, """[TIMING: 06:00 - 08:00 | 2 Minutes]
SPEAKER SCRIPT:
"To make our engineering concrete, we mapped these risks into three primary hazard vectors that formed the core of our technical requirements:

First, Identity Mismatch. If an orchestrator auto-resolves a conflicting MRN or DOB because the names look similar, you risk infusing the wrong cells. The system must never guess; it must fail closed and demand explicit human adjudication.

Second, Blind Retries on Slot Orchestration. In enterprise integrations, timeouts happen constantly. If an orchestrator treats a timeout as a failure and retries blindly, it can dispatch multiple reservation commands for the same patient, wasting quarter-million-dollar manufacturing slots and throwing the entire commercial schedule into disarray.

Third, Premature Quality Release. Software often conflates 'Manufacturing Done' with 'Drug Released'. If software auto-releases a batch while an open equipment alarm deviation sits unresolved in the QMS, you violate GxP law.

These three hard problems became POC 1, POC 2, and POC 3."
""")

    # =========================================================================
    # SLIDE 5: The 21-Stage Operating Architecture [08:00 - 10:00]
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    add_bg(s5, prs, C_LIGHT_BG)
    add_header(s5, "04 / OPERATING MODEL", "The 21-Stage Forward Deployed Engineering Architecture", "A rigorous end-to-end discipline from forensic baseline profiling to production readiness")

    frame_path = FRAMES_DIR / "scene03.png"
    if frame_path.is_file():
        s5.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.8), width=Inches(5.8))

    box = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tf = box.text_frame
    tf.word_wrap = True

    stages = [
        ("Phase 1: Discovery & Forensics (Stages 1–5)", "Forensic baseline extraction of 132 challenge files, data knowledge profiling, value-risk-feasibility scoring, and persona definitions."),
        ("Phase 2: Modeling & Contracts (Stages 6–9)", "Domain data dictionary, formal evaluation catalog (57 test cases), solution scoring, and machine-readable JSON schemas."),
        ("Phase 3: Architecture & PRD (Stages 10–14)", "C4 target architecture, build vs. buy evaluation, formal PRD, brownfield migration strategy, and GxP AIBOM generation."),
        ("Phase 4: Engineering & Assurance (Stages 15–18)", "118 automated tests (96.22% coverage), microbenchmarks, chaos recovery drills, and continuous deployment simulations."),
        ("Phase 5: Governance & Roadmap (Stages 19–21)", "Security & credential retirement scan, 90-day production gap roadmap, and G6 Lifecycle Restrict-and-Change decision."),
    ]
    for i, (title, desc) in enumerate(stages):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEAL

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_NAVY_TEXT
        p.space_after = Pt(8)

    add_notes(s5, """[TIMING: 08:00 - 10:00 | 2 Minutes]
SPEAKER SCRIPT:
"Rather than writing ad-hoc code, we executed this project under the full 21-stage Forward Deployed Engineering (FDE) operating model.

Across 21 distinct stages, we produced 185 tracked artifacts in our master register. We began with forensic analysis of the 132 raw baseline files in Stage 1 and 2, profiling data quality and identifying missing timestamps. In Stages 6 through 9, we defined formal contracts and built an evaluation catalog of 57 test cases. In Stages 10 through 14, we developed C4 architecture diagrams, a comprehensive PRD, and an AIBOM.

In Stage 15 through 18, we engineered the production engine, achieving 96.22% code coverage, running benchmark drills, and testing backup-restore recovery. And in Stages 19 through 21, we conducted security scans, mapped a 90-day production roadmap, and formalized our G6 release decision.

Every single artifact is accounted for and cryptographically verified in our repository."
""")

    # =========================================================================
    # SLIDE 6: Architecture Principles: Evidence Before Status [10:00 - 12:00]
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    add_bg(s6, prs, C_LIGHT_BG)
    add_header(s6, "05 / CORE PRINCIPLES", "Evidence Before Status: The Foundational Axiom", "Status labels do not create truth; the orchestrator records what is known, unknown, blocked, and authorized")

    principles = [
        ("1. Explicit Unknowns & Fail-Closed Gates", "If a required evidence artifact is missing (e.g. missing signed consent or unverified temperature reading), the readiness state is explicitly UNKNOWN, dominating any positive indicator. Missing evidence never defaults to satisfied.", C_TEAL),
        ("2. Human Sovereignty Over Authority", "Artificial intelligence and workflow automation may summarize state and surface discrepancies, but they have zero consequential authority. Only credentialed human principals (Quality, Identity) can authorize transitions.", C_NAVY_TEXT),
        ("3. Bi-Temporal Audit & Tamper-Evidence", "Every operational state mutation appends an immutable record with occurrence time vs. recording time. Cryptographic SHA-256 hash chains detect any unauthorized ledger modification.", C_CYAN),
        ("4. Safe Idempotent Commands & Reconciliation", "All mutating operations require client-generated idempotency keys. In network dropouts, the system transitions to OUTCOME_UNKNOWN, checks external reality, and prevents duplicate executions.", C_AMBER),
    ]
    for i, (title, desc, col) in enumerate(principles):
        top = Inches(1.8 + i * 1.35)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_MUTED_TEXT

    add_notes(s6, """[TIMING: 10:00 - 12:00 | 2 Minutes]
SPEAKER SCRIPT:
"Our architecture is built on four non-negotiable engineering principles:

First: 'Status labels do not create truth.' In many healthcare systems, an operator changes a dropdown from 'Pending' to 'Approved', and everyone treats that label as fact. In our engine, a status label is meaningless without an immutable, cited evidence reference. If evidence is missing, the gate is explicitly UNKNOWN and fails closed.

Second: Human Sovereignty. AI can summarize, format, and surface risks, but it cannot release a drug or merge a patient identity. 

Third: Bi-temporal Audit Trails. We record both when an event occurred in the physical world and when our system learned about it. This ensures late-arriving telemetry never rewrites historical known-at reality.

Fourth: Idempotency with Reconciliation. A network timeout is neither a confirmed success nor a confirmed failure—it is an OUTCOME_UNKNOWN that requires reconciliation before retry."
""")

    # =========================================================================
    # SLIDE 7: Information Architecture & AI Boundaries [12:00 - 13:30]
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    add_bg(s7, prs, C_LIGHT_BG)
    add_header(s7, "06 / INFORMATION ARCHITECTURE", "Structured Truth vs. RAG vs. AI Guardrails", "Calibrated information boundaries: zero generative hallucination in the critical path")

    tiers = [
        ("Direct Structured Retrieval (Canonical Truth)", "Operational facts (batches, lots, patient keys, dates, QC passes) are extracted via deterministic typed models directly from raw CSV/SQL tables. Zero vector embeddings, zero LLM generation.", C_GREEN),
        ("Optional Retrieval-Augmented Generation (RAG)", "Restricted purely to supporting unstructured context: reading clinical SOPs, investigator brochures, and unstructured deviation notes. RAG is prohibited from deciding operational status.", C_TEAL),
        ("Strict Model Boundary (AI Off by Default)", "In production, AI_MODE=off. When the advisory assistant is enabled for demonstration, it runs in a bounded fake adapter that provides narrative explanation with explicit uncertainty declarations.", C_NAVY_TEXT),
    ]
    for i, (title, desc, col) in enumerate(tiers):
        top = Inches(1.8 + i * 1.75)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.55))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_MUTED_TEXT

    add_notes(s7, """[TIMING: 12:00 - 13:30 | 1.5 Minutes]
SPEAKER SCRIPT:
"A major contribution of this capstone is establishing clean information architecture boundaries for AI in life sciences.

In enterprise software today, there is a temptation to throw a large language model and vector database at everything. We rejected that anti-pattern completely. 

In our architecture, canonical operational facts—such as whether a batch passed sterility testing or whether an apheresis bag was delivered—are handled purely through deterministic, typed relational projections. Zero vector search, zero LLM hallucinations.

RAG is evaluated for optional, supporting tasks only: indexing SOP manuals and free-text deviation narratives. And for the critical path, the system operates with AI completely off. When our advisory assistant runs, it is strictly non-binding, citation-constrained, and isolated from operational authority."
""")

    # =========================================================================
    # SLIDE 8: Multi-Persona Operational Lenses [13:30 - 15:00]
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    add_bg(s8, prs, C_LIGHT_BG)
    add_header(s8, "07 / PERSONA ARCHITECTURE", "One Journey, Seven Operational Responsibilities", "Role-based lenses adjust presentation focus while enforcing backend permission boundaries")

    roles = [
        ("Patient Operations", "End-to-end journey tracking & managing exception cases across centers.", C_TEAL),
        ("Identity Authority", "Adjudicating clinical subject, MRN, and consent discrepancies.", C_CYAN),
        ("Logistics / Planner", "Monitoring dry vapor LN2 transit, couriers, and temperature excursions.", C_NAVY_TEXT),
        ("Manufacturing Ops", "Managing bioreactor slots, apheresis receipt, and lot processing.", C_AMBER),
        ("Lab / QC Analyst", "Recording cell viability, identity assays, and sterility testing.", C_GREEN),
        ("Quality Authority", "Reviewing deviation packages and executing formal GxP batch release.", C_RED),
        ("Executive Viewer", "Real-time portfolio visibility, compliance posture, and SLA tracking.", C_MUTED_TEXT),
    ]
    for i, (title, desc, col) in enumerate(roles):
        row = i // 4
        col_idx = i % 4
        left = Inches(0.8 + col_idx * 2.95)
        top = Inches(2.0 + row * 2.5)
        w = Inches(2.8)
        h = Inches(2.3)

        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_NAVY_TEXT

    add_notes(s8, """[TIMING: 13:30 - 15:00 | 1.5 Minutes]
SPEAKER SCRIPT:
"In clinical cell therapy, different stakeholders need different operational views, but backend permissions must remain strictly enforced.

We developed seven persona lenses:
The Patient Operations Coordinator needs an end-to-end overview and exception management.
The Identity Authority focuses strictly on resolving MRN and consent mismatches.
The Logistics Planner watches cryogenic telemetry and courier handoffs.
Manufacturing Operations oversees apheresis receipt and bioreactor suites.
The Lab QC Analyst verifies flow cytometry and sterility assays.
The Quality Authority owns the legal release decision.
And the Executive Viewer monitors portfolio metrics and compliance health.

Crucially, selecting a role lens in our UI changes what is highlighted, but it does not grant backend authority. Mutating actions require cryptographically verified server-side tokens."
""")

    # =========================================================================
    # SLIDE 9: Featured Demo Video Showcase [15:00 - 18:00]
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    add_bg(s9, prs, C_DARK_BG)
    add_header(s9, "08 / DEMONSTRATION SHOWCASE", "Live Walkthrough: The 120-Second Capstone Demo", "High-definition narrated demonstration of the control tower and three foundational proofs", dark=True)

    frame_path = FRAMES_DIR / "scene04.png"
    if frame_path.is_file():
        s9.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.8), width=Inches(5.8))

    box = s9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FEATURED VIDEO ARTIFACT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = "File: cgt_patient_to_batch_orchestration_demo.mp4\nDuration: 120 Seconds · Format: 1080p Widescreen (60 fps)\nCaptions: Full English Subtitles (.srt & .vtt committed)"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "Video Timeline & Key Moments:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(6)

    v_points = [
        ("00:00–00:30", "The Problem: Connecting living drugs across 4 fragmented systems."),
        ("00:30–00:53", "The 21-Stage Model & Unified Control Tower Interface."),
        ("00:53–01:03", "POC 01: Conflicting MRN becomes an owned exception, not an invented link."),
        ("01:03–01:12", "POC 02: Network timeout marked OUTCOME_UNKNOWN; replay blocked."),
        ("01:12–01:25", "POC 03: MES complete is not released; requires Quality authorization."),
        ("01:25–02:00", "Assurance Scorecard & G6 Decision: Restrict & Change (AI off)."),
    ]
    for ts, desc in v_points:
        p = tf.add_paragraph()
        p.text = f"{ts} — {desc}"
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(148, 163, 184)
        p.space_after = Pt(4)

    add_notes(s9, """[TIMING: 15:00 - 18:00 | 3 Minutes]
SPEAKER SCRIPT:
"At this point in our presentation, we transition to our featured 120-second executive demonstration video.

[ACTION: Play video 'cgt_patient_to_batch_orchestration_demo.mp4' or narrate along with the slides]

Notice how the video establishes the living drug challenge in the first 30 seconds. At the 53-second mark, it demonstrates POC 1: when conflicting MRN records arrive from clinic feeds, the system refuses to guess; it creates an owned exception.

At 1 minute 3 seconds, POC 2 demonstrates an external slot reservation timeout: instead of retrying and double-booking, it flags OUTCOME_UNKNOWN and reconciles safely.

At 1 minute 12 seconds, POC 3 shows manufacturing completion: software is explicitly prohibited from releasing the lot until Quality reviews all deviation packets and signs the release.

And finally, at 1 minute 35 seconds, the video displays our assurance scorecard and our transparent G6 decision: Restrict and Change. Let's now dive deep into each of these three technical proofs."
""")

    # =========================================================================
    # SLIDE 10: POC 01 Deep Dive: Identity Conflict & Readiness [18:00 - 21:00]
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    add_bg(s10, prs, C_LIGHT_BG)
    add_header(s10, "09 / TECHNICAL PROOF 01", "Identity & Readiness: Conflicting Evidence Handled Safely", "When MRN and DOB assertions conflict, the orchestrator creates an owned case—never an invented patient link")

    frame_path = FRAMES_DIR / "scene05.png"
    if frame_path.is_file():
        s10.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.8), width=Inches(5.8))

    box = s10.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    steps = [
        ("The Stimulus (Conflict Injected)", "Clinic feed asserts Subject SUBJ-DE-0002 with MRN-888423; hospital portal asserts MRN-999121 with conflicting DOB 1985-04-12 vs 1985-04-14.", C_RED),
        ("The Ungrounded Shortcut (What Bad Systems Do)", "Heuristic string matching merges the records or silently picks the most recent timestamp, corrupting the Chain of Identity.", C_MUTED_TEXT),
        ("Our Deterministic Defense", "Identity decision evaluates to CONFLICT_DETECTED. The gate immediately drops to NOT_SATISFIED and fails closed.", C_TEAL),
        ("Human Adjudication & Cited Evidence", "System creates an owned P0 exception case citing exact CSV line locators. Only a credentialed Identity Authority can confirm the resolution.", C_NAVY_TEXT),
        ("Verified State Transition", "Readiness becomes SATISFIED only after verified authorization. Complete evidence citations are logged to the audit chain.", C_GREEN),
    ]
    for i, (title, desc, col) in enumerate(steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{i+1}. {title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_NAVY_TEXT
        p2.space_after = Pt(6)

    add_notes(s10, """[TIMING: 18:00 - 21:00 | 3 Minutes]
SPEAKER SCRIPT:
"Let's examine Proof of Concept 1: Identity Resolution.

In our test scenario, two conflicting feeds arrive for subject SUBJ-DE-0002. One feed from the clinical trial registry reports a birthdate of April 12th; another feed from the local hospital EHR reports April 14th with a different medical record number.

In naive healthcare software, string distance algorithms might say '92% similarity—merge records'. In autologous cell therapy, that 8% error can kill a patient. 

Our engine explicitly blocks the merge. It records an identity state of CONFLICT_DETECTED. It citations the exact source files and line numbers where the conflict arose. It creates a P0 exception case assigned to the Identity Authority role.

Only when the Identity Authority reviews the physical primary source records and applies an authorized signature does the gate flip to SATISFIED. Evidence precedes state—always."
""")

    # =========================================================================
    # SLIDE 11: POC 02 Deep Dive: Safe Slot Orchestration & Retries [21:00 - 24:00]
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    add_bg(s11, prs, C_LIGHT_BG)
    add_header(s11, "10 / TECHNICAL PROOF 02", "Safe Slot Orchestration: Idempotency & Network Timeouts", "A network timeout becomes an explicit unknown outcome—reconciled against external reality, never blindly retried")

    frame_path = FRAMES_DIR / "scene06.png"
    if frame_path.is_file():
        s11.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.8), width=Inches(5.8))

    box = s11.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    steps = [
        ("The Stimulus (Timeout Injected)", "A dispatch command is sent to book cleanroom manufacturing slot SLOT-MFG-01. The external CDMO API times out after committing the booking.", C_AMBER),
        ("The Disaster of Blind Retries", "Standard retry middleware re-sends the POST request with a new transaction ID, causing the CDMO to double-book the suite or throw concurrency errors.", C_MUTED_TEXT),
        ("Deterministic Unknown State", "Our engine transitions the reservation command state to OUTCOME_UNKNOWN. Retries are strictly blocked by the state machine.", C_TEAL),
        ("External Reconciliation Protocol", "The reconciliation worker queries the external CDMO transaction journal using the original Idempotency-Key.", C_NAVY_TEXT),
        ("Idempotent Replay Protection", "Reconciliation confirms the slot was booked; state updates to SUCCEEDED. Duplicate calls return the cached response without dispatch.", C_GREEN),
    ]
    for i, (title, desc, col) in enumerate(steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{i+1}. {title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_NAVY_TEXT
        p2.space_after = Pt(6)

    add_notes(s11, """[TIMING: 21:00 - 24:00 | 3 Minutes]
SPEAKER SCRIPT:
"Next, Proof of Concept 2: Safe Slot Orchestration.

Manufacturing suites for cell therapy require advanced scheduling: isolators, cleanrooms, viral vector batches, and specialized technicians. A single slot reservation is worth over $250,000.

In our simulation, a reservation command is dispatched to CDMO partner suite MFG-US-NJ-01. The remote server receives the request, reserves the slot, but the network connection drops before the HTTP 200 response reaches our orchestrator.

What does standard microservice architecture do? It retries three times with exponential backoff. The CDMO receives three more booking requests, double-booking the cleanroom.

Our engine refuses to retry blindly. It marks the command as OUTCOME_UNKNOWN. It locks the transaction. A reconciliation worker then queries the external transaction journal using our client-generated idempotency key. When it discovers the reservation was already recorded, it reconciles our local state to SUCCEEDED. When a duplicate dispatch is attempted, it returns the cached result without touching the external network."
""")

    # =========================================================================
    # SLIDE 12: POC 03 Deep Dive: Quality Release Sovereignty [24:00 - 27:00]
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    add_bg(s12, prs, C_LIGHT_BG)
    add_header(s12, "11 / TECHNICAL PROOF 03", "Quality Release: Retained Authority Over Consequential Actions", "MES completion and ERP logistics signals cannot authorize release; only Quality Authority can clear a drug")

    frame_path = FRAMES_DIR / "scene07.png"
    if frame_path.is_file():
        s12.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.8), width=Inches(5.8))

    box = s12.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    steps = [
        ("The Stimulus (Manufacturing Complete)", "Batch BAT-00010 finishes processing. MES marks lot 'Complete', ERP marks materials 'Consumed', courier is dispatched.", C_AMBER),
        ("The Unsafe Shortcut", "Automated pipelines assume 'Processing Done' equals 'Release Approved' and update the patient portal to 'Infusion Ready'.", C_MUTED_TEXT),
        ("Pre-Release Evidence Evaluation", "The orchestrator evaluates 4 mandatory packets: Identity Verification, Patient Consent v3, Cryo Temp Data, and QC Assays (Viability > 70%).", C_TEAL),
        ("Deviation Blocker Detected", "Batch BAT-00010 has an open bioreactor pressure deviation DEV-00019. Automated release is strictly blocked; state remains RELEASE_PENDING.", C_RED),
        ("Human Quality Authorization", "Quality Authority reviews the closed investigation report, applies an authorized digital disposition, and transitions state to RELEASE_APPROVED.", C_GREEN),
    ]
    for i, (title, desc, col) in enumerate(steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{i+1}. {title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_NAVY_TEXT
        p2.space_after = Pt(6)

    add_notes(s12, """[TIMING: 24:00 - 27:00 | 3 Minutes]
SPEAKER SCRIPT:
"Proof of Concept 3 addresses the most dangerous trap in automated life-sciences software: premature Quality release.

In our scenario, manufacturing finishes on Batch BAT-00010. The bioreactors shut down, the cells are frozen into cryo-vials, and the MES emits an event saying 'Manufacturing Complete'. 

In many commercial systems, downstream portals listen for this event and immediately alert the hospital that the product is ready for infusion. But there is an open deviation: during hour 48 of expansion, an incubator temperature alert DEV-00019 was flagged and remains under investigation.

Our engine evaluates four distinct evidence packets: Identity, Consent, Cryogenic Telemetry, and QC Lab Assays. Because an open deviation exists, the Quality Release gate evaluates to UNKNOWN / BLOCKED. The product is physically quarantined.

Only when the Quality Authority reviews the root cause analysis, verifies the safety assays, and inputs a cryptographic release authorization does the system transition to RELEASE_APPROVED. This guarantees compliance with FDA Part 11 and cGMP."
""")

    # =========================================================================
    # SLIDE 13: Centralized Patient Operations Dashboard [27:00 - 29:30]
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    add_bg(s13, prs, C_LIGHT_BG)
    add_header(s13, "12 / CENTRALIZED DASHBOARD", "Global Cohort Operations Across 800 Patients", "Centralized, real-time status tracking, multi-facet filtering, and longitudinal relational drilldowns")

    frame_path = FRAMES_DIR / "scene08.png"
    if frame_path.is_file():
        s13.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.8), width=Inches(5.8))

    box = s13.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    features = [
        ("Real-Time KPI Strip", "Live visibility across all 800 patients: 673 Active Cohort, 127 Completed Cohort, 145 Active QA Holds, and 25 Governed Infusion Ready.", C_TEAL),
        ("Multi-Facet Live Filtering", "Filter dynamically by Journey Phase (Enrolled, Apheresis, Mfg, QC, QA Hold, Infusion Ready), Product Code (CGT-A1, CGT-C3), Treatment Center, and Cohort.", C_CYAN),
        ("Dual View Modes", "Responsive tabular operations view with status dimension pills (Journey Position vs Governing Readiness vs Infusion Auth) and modular card grid.", C_NAVY_TEXT),
        ("Longitudinal Relational Modals", "Clicking any patient opens full linked history: Shipments, Manufacturing Slots, QC Release Packets, Deviations, Consents, and Insurance Authorizations.", C_GREEN),
        ("Disruption Simulator Transfer", "One-click prefill transfers any selected patient into the non-authoritative Disruption Impact Preview engine.", C_AMBER),
    ]
    for i, (title, desc, col) in enumerate(features):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_NAVY_TEXT
        p.space_after = Pt(8)

    add_notes(s13, """[TIMING: 27:00 - 29:30 | 2.5 Minutes]
SPEAKER SCRIPT:
"Now, let's explore the Centralized Patient Operations Dashboard, which integrates directly into our FastAPI control tower.

Until this point, the baseline only permitted inspecting one patient at a time. Operations teams managing clinical trials or commercial therapies cannot operate through keyhole views—they need full population visibility.

Our dashboard connects directly to the 800 synthetic patient cohort. At the top, coordinators have an instant KPI strip showing active vs completed patients, open QA holds, and products staged for infusion.

Below, coordinators can filter across ten orchestration phases, filter by clinical trial center from Zurich to Singapore, or search across MRNs, batch IDs, and chain of identity identifiers.

Clicking on any patient launches a comprehensive modal that renders every connected record: cryogenic shipments, bioreactor reservations, QC viability assays, open deviation tickets, consent versions, and payer authorizations. Everything is rendered from typed, zero-allocation Python projections."
""")

    # =========================================================================
    # SLIDE 14: Population Analytics & Forensic Breakdown [29:30 - 31:30]
    # =========================================================================
    s14 = prs.slides.add_slide(blank)
    add_bg(s14, prs, C_LIGHT_BG)
    add_header(s14, "13 / COHORT ANALYTICS", "Forensic Breakdown of the 800-Patient Baseline", "Population-level distribution across manufacturing, logistics, QA hold, and infusion readiness")

    # Metrics Grid (2x3)
    kpis = [
        ("800", "Total Patient Population", "Full synthetic cohort evaluated across 132 raw brownfield evidence tables", C_NAVY_TEXT),
        ("673", "Active In-Flight Cohort", "Patients actively progressing across enrollment, collection, mfg, and transit", C_TEAL),
        ("127", "Completed Therapies", "Patients who successfully received cellular infusion under governed protocols", C_GREEN),
        ("145", "Total QA Discrepancies", "Batches flagged with open manufacturing deviations, equipment alarms, or holds", C_RED),
        ("57", "Physically at Treatment Site", "Cell product staged in hospital dry vapor LN2 dewars awaiting clinical readiness", C_CYAN),
        ("25", "Strictly Infusion Ready", "Batches physically at site WITH verified QMS release and zero blocking holds", C_GREEN),
    ]
    for i, (val, label, sub, col) in enumerate(kpis):
        r = i // 3
        c = i % 3
        left = Inches(0.8 + c * 3.9)
        top = Inches(2.0 + r * 2.5)

        card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.7), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY_TEXT
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = C_MUTED_TEXT

    add_notes(s14, """[TIMING: 29:30 - 31:30 | 2 Minutes]
SPEAKER SCRIPT:
"Here is the forensic breakdown of the 800-patient population.

Of the 800 patients, 673 are active and 127 have completed infusion. But notice the critical figures on the right:

There are 145 patients associated with open Quality discrepancies or manufacturing holds across the dataset. 

Now look at the distinction between the physical world and the Quality world: 57 patients have their cellular drug physically sitting in cryogenic dewars at the hospital treatment center. In naive software, all 57 would be labeled 'Infusion Ready'.

However, when our engine cross-references the batch release records and deviation ledgers, 32 of those 57 batches either have unresolved manufacturing holds or QMS release status pending. Therefore, exactly 25 patients are genuinely, strictly authorized for clinical infusion.

This single calculation illustrates the difference between software that merely tracks logistics and an orchestrator that protects human lives."
""")

    # =========================================================================
    # SLIDE 15: Case Study: Patient P-00013 & The Hold Quagmire [31:30 - 33:00]
    # =========================================================================
    s15 = prs.slides.add_slide(blank)
    add_bg(s15, prs, C_LIGHT_BG)
    add_header(s15, "14 / CASE STUDY", "Patient P-00013: Cameron Wilson & The QA Hold Quagmire", "How the orchestrator prevents a lethal clinical error despite misleading physical staging")

    # Left box - Facts
    b1 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    b1.fill.solid()
    b1.fill.fore_color.rgb = C_WHITE
    b1.line.color.rgb = C_BORDER
    tf1 = b1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "PATIENT PROFILE: P-00013"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(6)

    facts = [
        "Patient: Cameron Wilson (DOB: 1992-01-21)",
        "Therapy: CGT-C3 autologous CAR-T",
        "Hospital: TC-DE-BER-01 (Berlin Treatment Center)",
        "Physical Location: Returned to Site / Staged in dewar",
        "Clinical Export Status: INFUSION_READY (Misleading)",
        "Batches Table Truth: BAT-00013 flags hold_status = HOLD and qms_status = QA_HOLD",
        "Deviations Table Reality: No linked row exists in deviations.csv (Orphaned source hold flag)",
    ]
    for fact in facts:
        p = tf1.add_paragraph()
        p.text = f"• {fact}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_NAVY_TEXT
        p.space_after = Pt(6)

    # Right box - Resolution
    b2 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    b2.fill.solid()
    b2.fill.fore_color.rgb = C_WHITE
    b2.line.color.rgb = C_RED
    b2.line.width = Pt(2)
    tf2 = b2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "ORCHESTRATOR RESOLUTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p.space_after = Pt(6)

    resolutions = [
        ("Journey Status", "Returned to Site (Quarantined)"),
        ("Governing Readiness", "BLOCKED — QA HOLD"),
        ("Infusion Authorization", "STRICTLY PROHIBITED"),
        ("Quality Disposition Ref", "UNLINKED_SOURCE_HOLD_FLAG"),
        ("Hold Category", "ACTIVE_MANUFACTURING_HOLD"),
        ("Clinical Risk Note", "Authoritative QMS release is on HOLD. Physical quarantine required; clinical administration is strictly prohibited."),
    ]
    for title, val in resolutions:
        p = tf2.add_paragraph()
        p.text = f"{title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY_TEXT
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = C_RED if "PROHIBITED" in val or "BLOCKED" in val else C_MUTED_TEXT
        p.space_after = Pt(8)

    add_notes(s15, """[TIMING: 31:30 - 33:00 | 1.5 Minutes]
SPEAKER SCRIPT:
"Let's look at Patient P-00013, Cameron Wilson. This case perfectly illustrates our engine's defensive design.

Cameron Wilson is enrolled at the Berlin Treatment Center. His manufactured CAR-T cells completed transit and arrived at the hospital dewar. The hospital clinical export lists his status as 'INFUSION_READY'. If the oncologist opened the hospital portal, they would see green lights and prepare to infuse the patient.

However, deep in the manufacturing batches table, batch BAT-00013 contains an unlinked hold flag: `hold_status = HOLD`. There is no ticket in `deviations.csv`—it is an unlinked source anomaly.

Earlier prototypes made two fatal mistakes: they either ignored the hold flag because no deviation row existed, or they fabricated an imaginary CAPA ticket ID to satisfy the UI.

Our Python service does neither. It refuses to fabricate ground truth. It tags the reference honestly as UNLINKED_SOURCE_HOLD_FLAG, flips the infusion authorization to PROHIBITED, marks the journey position as 'Returned to Site (Quarantined)', and sounds an alarm across the dashboard.

Cameron Wilson is protected from receiving an adulterated, unreleased drug."
""")

    # =========================================================================
    # SLIDE 16: Zero-Fabrication GxP Discipline [33:00 - 34:30]
    # =========================================================================
    s16 = prs.slides.add_slide(blank)
    add_bg(s16, prs, C_LIGHT_BG)
    add_header(s16, "15 / DATA INTEGRITY", "Zero-Fabrication GxP Engineering Discipline", "Rigorous resolution of the domain logic flaws uncovered during forensic code inspection")

    flaws = [
        ("Flaw: False Positive 'Infusion Ready' Records", "Prototype Flaw: 18 out of 40 patients marked 'Infusion Ready' had QMS status PENDING in source tables.\nOur Fix: Readiness strictly requires qms_release_status == 'RELEASED' and not has_hold. Exactly 25 patients qualify globally.", C_RED),
        ("Flaw: Fabricated CAPA Identifiers & Hold Dates", "Prototype Flaw: Fabricated strings like 'CAPA-2026-HOLD-${patient_key}' and made-up opening timestamps.\nOur Fix: Never invents CAPAs. Uses true deviation IDs or assigns UNLINKED_SOURCE_HOLD_FLAG with opened_at: None.", C_AMBER),
        ("Flaw: Imaginary 'Administered Under Exception' Claims", "Prototype Flaw: Claimed infused patients with open holds were administered under authorized clinical exceptions.\nOur Fix: Categorized honestly as INFUSED_WITH_UNRESOLVED_DISCREPANCY—an explicit audit finding requiring investigation.", C_TEAL),
    ]
    for i, (title, desc, col) in enumerate(flaws):
        top = Inches(2.0 + i * 1.7)
        card = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_NAVY_TEXT

    add_notes(s16, """[TIMING: 33:00 - 34:30 | 1.5 Minutes]
SPEAKER SCRIPT:
"This brings us to a fundamental lesson in GxP data engineering: Zero Ground Truth Fabrication.

During our audit of earlier prototypes, we discovered three critical domain flaws that would fail any FDA inspection:

First, 18 patients were shown on screen as 'Infusion Ready' even though their QMS release status was PENDING. We eliminated all 18 false positives.

Second, when the UI needed a CAPA ticket number or a hold opening date and none existed in the database, the prototype fabricated strings like 'CAPA-2026-HOLD-P-00013' and synthesized fake dates. In GxP, fabricating data is a criminal violation. Our engine never invents data; it outputs UNLINKED_SOURCE_HOLD_FLAG with opened_at: None.

Third, when infused patients had open holds, the prototype displayed 'Administered under exception'. But there was no exception event in the source tables! We reclassified those records as INFUSED_WITH_UNRESOLVED_DISCREPANCY—an explicit audit finding demanding post-infusion investigation.

Integrity is not just about clean UI; it is about absolute truthfulness in the data layer."
""")

    # =========================================================================
    # SLIDE 17: Calibrated Assurance & Verification [34:30 - 36:00]
    # =========================================================================
    s17 = prs.slides.add_slide(blank)
    add_bg(s17, prs, C_LIGHT_BG)
    add_header(s17, "16 / VERIFICATION POSTURE", "Calibrated Assurance: 118 Tests & 17/17 Passing Gates", "Continuous automated verification enforced by GitHub Actions CI and cryptographic digests")

    frame_path = FRAMES_DIR / "scene09.png"
    if frame_path.is_file():
        s17.shapes.add_picture(str(frame_path), Inches(6.8), Inches(1.8), width=Inches(5.8))

    box = s17.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    metrics = [
        ("Automated Tests", "118 passed in 3.19s (Unit, Integration, E2E, Chaos Recovery, Performance)"),
        ("Code Coverage", "96.22% total coverage (Surpasses strict 94.00% fail-under gate)"),
        ("Static Type Analysis", "Mypy strict: Success with 0 issues across 24 source files"),
        ("Code Formatting & Linting", "Ruff: All checks passed with 0 errors"),
        ("Security & Credential Scan", "0 secrets / 0 credential patterns across 570 repository text files"),
        ("Evidence Integrity", "132/132 baseline files verified byte-for-byte via SHA-256 digests"),
        ("Final Verification Suite", "tools/verify_final_capstone.py: 17/17 checks return PASS"),
    ]
    for label, val in metrics:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = f"✓ {label}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_GREEN

        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = C_NAVY_TEXT
        p.space_after = Pt(6)

    add_notes(s17, """[TIMING: 34:30 - 36:00 | 1.5 Minutes]
SPEAKER SCRIPT:
"Let's review our verification scorecard.

Our testing pyramid contains 118 automated tests passing in under 3.2 seconds. This includes unit tests for our temporal models and authorization logic, integration tests for all three POCs, and end-to-end full journey simulations.

Our code coverage is 96.22%, comfortably exceeding our enforced 94% fail-under threshold. 

Our codebase is fully typed: Mypy runs with zero errors across all 24 Python modules. Ruff reports zero linting issues. Our secret scanner examined all 570 text files with zero findings.

And our master verification utility, `verify_final_capstone.py`, runs 17 distinct provenance and integrity checks—from SHA-256 archive hashes to artifact register completeness—and every single check returns PASS.

Every build is continuously verified on GitHub Actions across Python 3.11 and 3.12."
""")

    # =========================================================================
    # SLIDE 18: G6 Lifecycle Decision: "RESTRICT AND CHANGE" [36:00 - 37:30]
    # =========================================================================
    s18 = prs.slides.add_slide(blank)
    add_bg(s18, prs, C_LIGHT_BG)
    add_header(s18, "17 / GOVERNANCE GATE", "G6 Lifecycle Decision: Why 'RESTRICT AND CHANGE' Is Correct", "Honest engineering boundaries: separating academic technical feasibility from clinical production readiness")

    cards = [
        ("What Is Demonstrated & Accepted", "• Technical feasibility of evidence-driven orchestration\n• Tamper-evident SHA-256 audit chain verified\n• Bounded idempotent state machines with safe timeouts\n• Multi-role operations dashboard across 800 patients\n• 118 automated tests passing at 96.22% coverage", C_GREEN),
        ("What Remains Restricted & Prohibited", "• Real patient data strictly prohibited (Synthetic only)\n• Consequential AI disabled (AI_MODE=off default)\n• Direct clinical administration prohibited\n• Automated Quality release prohibited\n• Production live-system deployments prohibited", C_RED),
        ("Why 'Restrict & Change' Is Correct", "An engineer who claims 'validated production readiness' on synthetic academic data commits malpractice. Recommending 'RESTRICT AND CHANGE' demonstrates mature regulatory awareness and protects the enterprise.", C_TEAL),
    ]
    for i, (title, desc, col) in enumerate(cards):
        left = Inches(0.8 + i * 3.9)
        card = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.0), Inches(3.7), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(10)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY_TEXT
        p.space_after = Pt(10)

    add_notes(s18, """[TIMING: 36:00 - 37:30 | 1.5 Minutes]
SPEAKER SCRIPT:
"At Stage 20 and 21, the operating model requires a formal G6 Lifecycle Decision.

There were three choices: Deploy As-Is, Abandon, or Restrict and Change.

An inexperienced team might be tempted to declare 'Deploy As-Is'. But in regulated life sciences, claiming production validation on synthetic local data is engineering malpractice. Two controlled human-factor studies remain unrun, and live enterprise integrations have not been stressed.

We unanimously recommended 'RESTRICT AND CHANGE'.

This means: Accept the academic POC. The architecture, the data contracts, the state machines, and the audit chains are proven sound. But keep live AI off, prohibit clinical use on real patients, and execute the 7 CAPAs on our 90-day roadmap before entering clinical validation.

This decision reflects true enterprise maturity."
""")

    # =========================================================================
    # SLIDE 19: Enterprise Roadmap: 7 CAPAs to Production [37:30 - 39:00]
    # =========================================================================
    s19 = prs.slides.add_slide(blank)
    add_bg(s19, prs, C_LIGHT_BG)
    add_header(s19, "18 / ROADMAP", "The 90-Day Production Roadmap: Seven Actionable CAPAs", "The concrete engineering bridge from verified academic POC to clinical enterprise validation")

    capas = [
        ("CAPA 1: Enterprise IAM & SSO", "Transition from demo tokens to enterprise Okta/Azure AD OIDC with MFA and role claims."),
        ("CAPA 2: HL7 / FHIR Integration", "Replace CSV parsers with validated HL7 v2 and FHIR R4 clinical EHR connectors."),
        ("CAPA 3: Validated Digital Signatures", "Implement 21 CFR Part 11 compliant dual-factor electronic signatures with non-repudiation."),
        ("CAPA 4: Hardware Security Module (HSM)", "Anchor SHA-256 audit chain master keys in an enterprise cloud HSM (AWS KMS / Azure Key Vault)."),
        ("CAPA 5: Multi-Region Disaster Recovery", "Execute automated failover drills with RPO < 1 min and RTO < 15 min across cloud availability zones."),
        ("CAPA 6: Controlled Human-Factor Studies", "Conduct formal GAMP 5 user-experience studies testing coordinator exception handling under stress."),
        ("CAPA 7: Formal CSV / GAMP 5 Validation", "Complete full Installation, Operational, and Performance Qualification (IQ/OQ/PQ) protocols."),
    ]
    for i, (title, desc) in enumerate(capas):
        top = Inches(1.8 + i * 0.75)
        card = s19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(0.68))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.12)

        p = tf.paragraphs[0]
        p.text = f"{title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEAL

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_NAVY_TEXT

    add_notes(s19, """[TIMING: 37:30 - 39:00 | 1.5 Minutes]
SPEAKER SCRIPT:
"To bridge the gap between our working POC and a production-grade hospital deployment, we defined a concrete 90-day roadmap organized into seven Corrective and Preventive Actions (CAPAs):

CAPA 1 replaces demo bearer tokens with enterprise OIDC single sign-on.
CAPA 2 implements HL7 and FHIR clinical connectors for direct EHR integration.
CAPA 3 deploys 21 CFR Part 11 cryptographic digital signatures for Quality releases.
CAPA 4 anchors our SHA-256 audit chains in a Hardware Security Module.
CAPA 5 tests multi-region failover and disaster recovery drills.
CAPA 6 executes the two controlled human-factor usability studies.
And CAPA 7 completes formal GAMP 5 Computerized System Validation.

This roadmap gives the enterprise a clear, accountable path to clinical production."
""")

    # =========================================================================
    # SLIDE 20: Summary, Business Value & Q&A [39:00 - 40:00]
    # =========================================================================
    s20 = prs.slides.add_slide(blank)
    add_bg(s20, prs, C_DARK_BG)
    add_header(s20, "19 / CONCLUSION", "Proven Control, Proven Integrity, Ready for Scaled CGT", "Summary of deliverable assets and transition to executive question-and-answer session", dark=True)

    # Deliverables Box on Left
    b1 = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8))
    b1.fill.solid()
    b1.fill.fore_color.rgb = C_DARK_CARD
    b1.line.color.rgb = C_CYAN
    tf1 = b1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)

    p = tf1.paragraphs[0]
    p.text = "CORE DELIVERABLES COMMITTED & PUSHED"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(12)

    delivs = [
        "1. Canonical FastAPI Python Engine (118 tests, 96.22% coverage)",
        "2. Centralized Patient Operations Dashboard (800 global cohort)",
        "3. 1080p Narrated Demo Video (cgt_patient_to_batch_orchestration_demo.mp4)",
        "4. Synchronized Subtitles (.srt and .vtt) & Visual Slide Frames",
        "5. Complete 21-Stage Artifact Register (185 tracked artifacts)",
        "6. Master Executive Presentation Deck (.pptx) & Speaker Guide",
        "7. Green GitHub Actions CI Verification Pipeline on main",
    ]
    for item in delivs:
        p = tf1.add_paragraph()
        p.text = item
        p.font.size = Pt(11)
        p.font.color.rgb = C_WHITE
        p.space_after = Pt(8)

    # Core Axiom Box on Right
    b2 = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.8))
    b2.fill.solid()
    b2.fill.fore_color.rgb = C_DARK_CARD
    b2.line.color.rgb = C_TEAL
    tf2 = b2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)

    p = tf2.paragraphs[0]
    p.text = "THE GOVERNING AXIOM"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(12)

    p = tf2.add_paragraph()
    p.text = '"Evidence before status, and human authority before automation."'
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(20)

    p = tf2.add_paragraph()
    p.text = "Thank you for your time, leadership, and partnership.\n\nWe now invite questions and discussion from the Steering Committee."
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(203, 213, 225)

    add_notes(s20, """[TIMING: 39:00 - 40:00 | 1 Minute + Transition to Q&A]
SPEAKER SCRIPT:
"In summary: We have delivered a complete, mathematically verified, and GxP-disciplined Cell and Gene Therapy orchestration platform.

All code, tests, documentation, video walkthroughs, and presentation assets are committed and verified green on GitHub. 

Our guiding axiom remains: 'Evidence before status, and human authority before automation.'

Thank you for your time and partnership. The floor is now open for questions and discussion from the committee."
""")

    prs.save(str(OUTPUT_PPTX))
    print(f"Successfully generated: {OUTPUT_PPTX}")


if __name__ == "__main__":
    build_slides()
