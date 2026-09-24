from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "Surya_FDE_Capstone_Bible.pdf"

NAVY = HexColor("#082F3A")
TEAL = HexColor("#0B8F82")
MINT = HexColor("#DDF5EE")
BLUE = HexColor("#DDEAF7")
AMBER = HexColor("#F8E9C7")
RED = HexColor("#A33B3B")
INK = HexColor("#17343D")
SLATE = HexColor("#526970")
LINE = HexColor("#C9D8D5")
PAPER = HexColor("#F7FAF9")
WHITE = colors.white


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverKicker",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=HexColor("#79D9C6"),
        tracking=1.8,
        alignment=TA_LEFT,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=29,
        leading=34,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=16,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=19,
        textColor=HexColor("#D8E8E5"),
        alignment=TA_LEFT,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=25,
        textColor=NAVY,
        spaceBefore=2,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="H2x",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=TEAL,
        spaceBefore=9,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyX",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=14.2,
        textColor=INK,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BodySmall",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.4,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHead",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.4,
        leading=9.4,
        textColor=WHITE,
    )
)
styles.add(
    ParagraphStyle(
        name="TableBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.15,
        leading=9.6,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="TableBodyBold",
        parent=styles["TableBody"],
        fontName="Helvetica-Bold",
        textColor=NAVY,
    )
)
styles.add(
    ParagraphStyle(
        name="Callout",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=15,
        textColor=NAVY,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="Tiny",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=6.6,
        leading=8.4,
        textColor=SLATE,
    )
)


def para(text: str, style: str = "BodyX") -> Paragraph:
    return Paragraph(text, styles[style])


def bullets(items: list[str]) -> list[Paragraph]:
    return [Paragraph(f"- {item}", styles["BodyX"]) for item in items]


def heading(title: str, kicker: str | None = None) -> list[Flowable]:
    items: list[Flowable] = []
    if kicker:
        items.append(Paragraph(kicker.upper(), ParagraphStyle(
            name=f"k-{title}", parent=styles["Tiny"], fontName="Helvetica-Bold",
            fontSize=7.2, leading=9, textColor=TEAL, spaceAfter=4, tracking=1.2
        )))
    items.append(para(title, "Section"))
    return items


def callout(text: str, background=MINT, accent=TEAL) -> Table:
    table = Table([[para(text, "Callout")]], colWidths=[170 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.8, accent),
        ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def info_cards(cards: list[tuple[str, str]], colors_: list | None = None) -> Table:
    colors_ = colors_ or [MINT, BLUE, AMBER]
    width = 170 * mm / len(cards)
    row = []
    for title, body in cards:
        row.append(Paragraph(f"<b>{title}</b><br/><font size='8'>{body}</font>", styles["BodyX"]))
    table = Table([row], colWidths=[width] * len(cards), hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.6, WHITE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]
    for index in range(len(cards)):
        commands.append(("BACKGROUND", (index, 0), (index, 0), colors_[index % len(colors_)]))
    table.setStyle(TableStyle(commands))
    return table


def data_table(headers: list[str], rows: list[list[str]], widths: list[float], font_size: float = 7.15) -> Table:
    header_cells = [para(item, "TableHead") for item in headers]
    body_rows = []
    for row in rows:
        body_rows.append([
            Paragraph(str(item), ParagraphStyle(
                name=f"cell-{font_size}-{index}",
                parent=styles["TableBody"],
                fontSize=font_size,
                leading=font_size + 2.3,
            ))
            for index, item in enumerate(row)
        ])
    table = Table([header_cells] + body_rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


class MindMap(Flowable):
    def __init__(self, width: float = 170 * mm, height: float = 104 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def _box(self, canvas, x, y, w, h, title, subtitle, fill):
        canvas.setFillColor(fill)
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.8)
        canvas.roundRect(x, y, w, h, 7, fill=1, stroke=1)
        canvas.setFillColor(NAVY)
        canvas.setFont("Helvetica-Bold", 8.2)
        canvas.drawString(x + 8, y + h - 15, title)
        canvas.setFillColor(SLATE)
        canvas.setFont("Helvetica", 6.8)
        words = subtitle.split()
        line = ""
        lines = []
        for word in words:
            candidate = f"{line} {word}".strip()
            if stringWidth(candidate, "Helvetica", 6.8) > w - 16:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)
        for index, value in enumerate(lines[:3]):
            canvas.drawString(x + 8, y + h - 28 - (index * 9), value)

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        center_x, center_y, center_w, center_h = 61 * mm, 42 * mm, 48 * mm, 22 * mm
        branches = [
            (3 * mm, 78 * mm, "1-4  UNDERSTAND", "Mandate, brownfield, problem, qualification", MINT),
            (116 * mm, 78 * mm, "5-8  MODEL", "Domain, data, evaluations, option selection", BLUE),
            (119 * mm, 33 * mm, "9-13  DESIGN", "Contracts, C4, agents, security, ADRs", AMBER),
            (92 * mm, 1 * mm, "14-18  PROVE", "Build, TEVV, operations, deployment, monitoring", MINT),
            (4 * mm, 10 * mm, "19-21  DECIDE", "Value, AIMS decision, closure and reuse", BLUE),
        ]
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.4)
        cx, cy = center_x + center_w / 2, center_y + center_h / 2
        for x, y, _, _, _ in branches:
            bw, bh = 50 * mm, 22 * mm
            c.line(cx, cy, x + bw / 2, y + bh / 2)
        for x, y, title, subtitle, fill in branches:
            self._box(c, x, y, 50 * mm, 22 * mm, title, subtitle, fill)
        c.setFillColor(NAVY)
        c.setStrokeColor(TEAL)
        c.setLineWidth(2)
        c.roundRect(center_x, center_y, center_w, center_h, 9, fill=1, stroke=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(cx, center_y + 13 * mm, "CENTRAL GOAL")
        c.setFont("Helvetica", 7)
        c.drawCentredString(cx, center_y + 8.5 * mm, "Safe evidence-driven")
        c.drawCentredString(cx, center_y + 5 * mm, "patient-to-batch journey")


class JourneyFlow(Flowable):
    def __init__(self, width: float = 170 * mm, height: float = 86 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        labels = [
            ("01", "Patient evidence", "Received and preserved"),
            ("02", "Identity conflict", "Detected and owned"),
            ("03", "Human identity decision", "Reviewed and applied"),
            ("04", "Readiness", "Evidence evaluated"),
            ("05", "Slot reservation", "Requested safely"),
            ("06", "Unknown outcome", "Reconciled, not replayed"),
            ("07", "Manufacturing and QC", "Evidence assembled"),
            ("08", "Quality authority", "Human release decision"),
            ("09", "Ready", "Traceable final outcome"),
        ]
        box_w, box_h = 52 * mm, 17 * mm
        positions = []
        columns = [0, 1, 2, 2, 1, 0, 0, 1, 2]
        for index in range(9):
            col = columns[index]
            row = index // 3
            x = col * 58 * mm
            y = self.height - (row + 1) * 26 * mm
            positions.append((x, y))
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.2)
        for index in range(8):
            x1, y1 = positions[index]
            x2, y2 = positions[index + 1]
            if y1 == y2 and x2 > x1:
                start = x1 + box_w
                end = x2
                center = y1 + box_h / 2
                c.line(start, center, end, center)
                c.line(end - 4, center + 3, end, center)
                c.line(end - 4, center - 3, end, center)
            elif y1 == y2:
                start = x1
                end = x2 + box_w
                center = y1 + box_h / 2
                c.line(start, center, end, center)
                c.line(end + 4, center + 3, end, center)
                c.line(end + 4, center - 3, end, center)
            else:
                center = x1 + box_w / 2
                end = y2 + box_h
                c.line(center, y1, center, end)
                c.line(center - 3, end + 4, center, end)
                c.line(center + 3, end + 4, center, end)
        for index, ((number, title, subtitle), (x, y)) in enumerate(zip(labels, positions)):
            fill = [MINT, BLUE, AMBER][index % 3]
            c.setFillColor(fill)
            c.setStrokeColor(LINE)
            c.roundRect(x, y, box_w, box_h, 6, fill=1, stroke=1)
            c.setFillColor(TEAL)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(x + 6, y + box_h - 11, number)
            c.setFillColor(NAVY)
            c.setFont("Helvetica-Bold", 7.6)
            c.drawString(x + 22, y + box_h - 11, title)
            c.setFillColor(SLATE)
            c.setFont("Helvetica", 6.5)
            c.drawString(x + 6, y + 5, subtitle)


def on_page(canvas, doc):
    canvas.saveState()
    if doc.page == 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setFillColor(TEAL)
        canvas.rect(0, A4[1] - 11 * mm, A4[0], 11 * mm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 7)
        canvas.drawCentredString(A4[0] / 2, A4[1] - 7 * mm, "SYNTHETIC ACADEMIC CAPSTONE - NO REAL PATIENT DATA - NOT FOR CLINICAL USE")
    else:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 12 * mm, A4[0], 12 * mm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 7.2)
        canvas.drawString(20 * mm, A4[1] - 7.7 * mm, "SURYA'S FDE CAPSTONE BIBLE")
        canvas.setFillColor(TEAL)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 7.7 * mm, "CGT PATIENT-TO-BATCH ORCHESTRATION")
        canvas.setStrokeColor(LINE)
        canvas.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
        canvas.setFillColor(SLATE)
        canvas.setFont("Helvetica", 6.8)
        canvas.drawString(20 * mm, 10 * mm, "Evidence before status. Human authority before automation.")
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


story: list[Flowable] = []

# Cover
story.extend([
    Spacer(1, 26 * mm),
    para("SURYA'S EXECUTIVE REFERENCE", "CoverKicker"),
    para("FDE Capstone<br/>Bible", "CoverTitle"),
    para("Cell and Gene Therapy<br/>Patient-to-Batch Orchestration", "CoverSub"),
    Spacer(1, 8 * mm),
])
cover_box = Table([[
    Paragraph(
        "<b>One fixed story.</b><br/>Understand the client ask, the 21-stage operating model, the working demonstration, the evidence and the honest lifecycle decision.",
        ParagraphStyle(name="cover-box", parent=styles["CoverSub"], fontSize=11, leading=17),
    )
]], colWidths=[150 * mm])
cover_box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#104754")),
    ("BOX", (0, 0), (-1, -1), 0.8, HexColor("#4DBDA8")),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 13),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
]))
story.append(cover_box)
story.extend([
    Spacer(1, 34 * mm),
    Paragraph("Prepared for Surya", ParagraphStyle(name="cover-name", parent=styles["CoverSub"], fontName="Helvetica-Bold", fontSize=12)),
    Paragraph("Version 1.0 | 15 September 2026", ParagraphStyle(name="cover-date", parent=styles["CoverSub"], fontSize=9)),
    Paragraph("FDE-Final-Capstone | Synthetic academic POC", ParagraphStyle(name="cover-scope", parent=styles["CoverSub"], fontSize=8)),
    PageBreak(),
])

# How to use
story.extend(heading("How to use this bible", "Start here"))
story.append(para("Do not try to memorize every artifact. First identify the type of question, route it to the correct stage, give the short answer and then point to the evidence."))
story.append(Spacer(1, 3 * mm))
story.append(info_cards([
    ("1. Hear the keyword", "Examples: DDD, C4, risk, data, test, deployment or ROI."),
    ("2. Route to a stage", "Use the five-phase memory map and quick question index."),
    ("3. Answer in four parts", "Yes or no; stage; what we did; evidence and limitation."),
]))
story.append(Spacer(1, 7 * mm))
story.append(callout("THE ANSWER FORMULA: Yes or no -> Stage -> What we did -> Evidence -> Honest limitation"))
story.extend([
    para("Use the sections in this order:", "H2x"),
    *bullets([
        "Pages 3-6: understand the business story and solution flow.",
        "Pages 7-12: understand all 21 FDE stages in five phases.",
        "Pages 13-17: understand the POCs, architecture, AI boundaries and evidence.",
        "Pages 18-22: prepare the live demo and answer reviewer questions.",
        "Final pages: limitations, lifecycle decision, glossary and one-page memory sheet.",
    ]),
    Spacer(1, 4 * mm),
    para("Golden rule", "H2x"),
    para("Never convert an academic POC result into a production, clinical, regulatory or financial claim. State what was demonstrated and what still requires external evidence."),
    PageBreak(),
])

# Executive summary and CGT
story.extend(heading("The capstone in one page", "Executive summary"))
story.append(callout("Build one safe, evidence-driven view of the journey from a specific patient to that patient's manufacturing batch."))
story.extend([
    para("What is CGT?", "H2x"),
    para("Cell and Gene Therapy (CGT) uses cells or genetic material to treat serious diseases. In this capstone's patient-specific journey, cells are collected for one patient, transported, manufactured into a treatment, Quality tested and returned for treatment."),
    para("Why is this difficult?", "H2x"),
    para("Clinical, scheduling, logistics, manufacturing, laboratory and Quality teams use different systems. Evidence can be delayed, missing or contradictory. A wrong identity link, duplicate reservation or unsupported release state can create serious risk."),
    para("What was delivered?", "H2x"),
])
story.append(info_cards([
    ("One Control Tower", "A controlled view of patient, batch, evidence, exceptions and decisions."),
    ("Three working POCs", "Identity readiness, safe slot orchestration and Quality release."),
    ("One honest decision", "Accept the academic POC; restrict real-data and production use."),
]))
story.extend([
    para("The result", "H2x"),
    para("All 21 FDE stages contain artifacts. All 77 automated tests pass. Fifty-five of 57 evaluation cases pass with zero failures; two human-study cases remain inconclusive. Twenty-five of 27 requirements are internally verified."),
    PageBreak(),
])

# Client ask
story.extend(heading("What the client is asking for", "Business need"))
story.append(para("The client needs a reliable way to answer five questions:"))
client_rows = [
    ["1", "Is this the correct patient?", "Identity and chain-of-identity evidence"],
    ["2", "Is the patient ready for manufacturing?", "Consent, eligibility, site and authorization evidence"],
    ["3", "Was the manufacturing slot reserved?", "Command state, external result and reconciliation"],
    ["4", "Can the batch be released?", "Manufacturing, QC, deviation, thermal and Quality authority"],
    ["5", "Why should we trust the answer?", "Citations, source provenance, decision owner and audit history"],
]
story.append(data_table(["#", "Client question", "Required proof"], client_rows, [10 * mm, 67 * mm, 93 * mm], 8.1))
story.extend([
    Spacer(1, 6 * mm),
    para("The engineering problem", "H2x"),
    para("The fragmented environment cannot always determine the current patient-to-batch state, why it is true, who is authorized to decide and what must happen next."),
    Spacer(1, 2 * mm),
])
story.append(info_cards([
    ("Identity risk", "Conflicting identifiers can create an unsafe patient link."),
    ("Operational risk", "Timeouts and retries can create duplicate external actions."),
    ("Authority risk", "Missing evidence or approval can be mistaken for readiness."),
]))
story.extend([
    Spacer(1, 7 * mm),
    para("The success condition", "H2x"),
    para("Every important state must show its evidence, uncertainty and accountable decision-maker. Unknown must remain unknown until it is resolved."),
    PageBreak(),
])

# Solution
story.extend(heading("The solution and its control principles", "Proposed answer"))
solution_rows = [
    ["Evidence before status", "A label is not truth. A state must cite current, permitted evidence."],
    ["Explicit unknowns", "Missing or conflicting evidence becomes UNKNOWN, not automatic approval."],
    ["Human authority", "Identity and Quality release require an authorized human decision."],
    ["Safe side effects", "Commands are idempotent; uncertain outcomes are reconciled before retry."],
    ["Owned exceptions", "Conflicts become cases with an owner, severity and resolution trail."],
    ["Auditability", "Important actions and decisions enter a tamper-evident audit chain."],
    ["AI independence", "The deterministic core works with AI off; AI can only recommend."],
]
story.append(data_table(["Principle", "Meaning in this capstone"], solution_rows, [55 * mm, 115 * mm], 8.0))
story.extend([
    Spacer(1, 6 * mm),
    callout("The Control Tower does not replace source systems or decision authorities. It coordinates evidence, state, exceptions and controlled actions across them."),
    Spacer(1, 5 * mm),
    para("What users see", "H2x"),
])
story.append(info_cards([
    ("Journey", "Enrollment through identity, slot, manufacturing, Quality and readiness."),
    ("Controls", "Human authorization, idempotency, audit validity and AI mode."),
    ("Assurance", "Stage, test, evaluation and requirement results with restrictions."),
]))
story.append(PageBreak())

# Journey flow
story.extend(heading("End-to-end patient-to-batch flow", "One path - no deviation"))
story.append(para("Always explain the capstone in this order. Do not begin with AI or architecture. Begin with the patient journey and the evidence problem."))
story.append(Spacer(1, 5 * mm))
story.append(JourneyFlow())
story.append(Spacer(1, 3 * mm))
journey_rows = [
    ["Identity", "Conflicting evidence creates a case", "Authorized human resolution"],
    ["Reservation", "Timeout creates an unknown result", "Reconcile before any repeat"],
    ["Release", "Evidence exists but authority is absent", "Quality decision remains mandatory"],
]
story.append(data_table(["Decision point", "Unsafe shortcut avoided", "Controlled response"], journey_rows, [35 * mm, 68 * mm, 67 * mm], 7.8))
story.append(PageBreak())

# Mind map
story.extend(heading("The 21-stage FDE mind map", "Navigation model"))
story.append(MindMap())
story.append(Spacer(1, 4 * mm))
story.append(data_table(
    ["Stages", "Question to remember", "Examples"],
    [
        ["1-4", "Why are we doing this?", "Mandate, brownfield, problem, value, regulation"],
        ["5-8", "What must the solution understand?", "DDD, data, evaluations, option selection"],
        ["9-13", "How should we design and govern it?", "Contracts, C4, agents, security, ADRs"],
        ["14-18", "Did we build, test and operate it?", "Code, POCs, TEVV, runbooks, deployment, monitoring"],
        ["19-21", "What was proven and what happens next?", "Value, AIMS, CAPA, lifecycle, retirement, reuse"],
    ],
    [22 * mm, 65 * mm, 83 * mm],
    7.9,
))
story.extend([
    Spacer(1, 5 * mm),
    callout("Memory sentence: Understand -> Model -> Design -> Prove -> Decide"),
    PageBreak(),
])

# Phase 1
story.extend(heading("Stages 1-4: Understand and frame", "Why are we doing this?"))
phase1 = [
    ["1", "Mandate and field immersion", "Define mission, scope, stakeholders, affected groups and decision rights.", "Charter, evidence policy, stakeholder map, RACI"],
    ["2", "Discover process and architecture", "Parse the supplied ZIP, reproduce the baseline and map current process, systems and risks.", "132-file inventory, forensic baseline, current-state architecture"],
    ["3", "Frame problem, root cause and value", "Use SCQA, root-cause analysis, KPIs and CTQs to prioritize the real problem.", "Problem frame, root causes, KPI baseline, success criteria"],
    ["4", "Triage regulation and qualify use case", "Define intended purpose, AI suitability, prohibited uses and human authority.", "Use-case cards, boundaries, G1 decision"],
]
story.append(data_table(["Stage", "Activity", "What we did", "Key evidence"], phase1, [13 * mm, 38 * mm, 68 * mm, 51 * mm], 7.35))
story.extend([
    Spacer(1, 6 * mm),
    para("Typical questions", "H2x"),
    *bullets([
        "What was the client asking for? -> Stages 1-3.",
        "How did you understand the legacy system? -> Stage 2.",
        "How did you define the problem and KPIs? -> Stage 3.",
        "Did you consider regulation and responsible AI before building? -> Stage 4.",
    ]),
    callout("Stage 4 rule: no application architecture is selected until domain, data, evaluation and option work in Stages 5-8 is complete.", AMBER, HexColor("#C98914")),
    PageBreak(),
])

# Phase 2
story.extend(heading("Stages 5-8: Model and select", "What must the solution understand?"))
phase2 = [
    ["5", "Model the domain", "Create the ubiquitous language, bounded contexts, aggregates, ownership, rules, events and state machines.", "DDD model and machine-readable domain specification"],
    ["6", "Qualify data and knowledge", "Assess quality, lineage, provenance, permissible use, representativeness and knowledge gaps.", "Profiles, inventories, source-trust and gap registers"],
    ["7", "Define evaluations, impacts and risks", "Freeze normal, failure, security, recovery and human-oversight cases before implementation.", "57-case catalog, thresholds, risk and impact assessment"],
    ["8", "Generate, test and select options", "Compare six options using spikes, TCO, provider/build-buy and weighted trade-offs.", "Selected deterministic evidence-driven Control Tower"],
]
story.append(data_table(["Stage", "Activity", "What we did", "Key evidence"], phase2, [13 * mm, 38 * mm, 68 * mm, 51 * mm], 7.35))
story.extend([
    Spacer(1, 6 * mm),
    para("DDD answer", "H2x"),
    callout("Yes. DDD was applied in Stage 5 through the glossary, bounded contexts, aggregates, business rules, domain events and canonical state machines."),
    Spacer(1, 5 * mm),
    para("Why this matters", "H2x"),
    para("DDD separates domain authority from software convenience. Clinical, manufacturing, scheduling and Quality meanings are explicit, so one technical service cannot silently redefine another function's truth."),
    PageBreak(),
])

# Phase 3
story.extend(heading("Stages 9-13: Design and approve", "How should we build and govern it?"))
phase3 = [
    ["9", "Information architecture", "Define evidence, event, command and recommendation contracts.", "Three versioned JSON schemas"],
    ["10", "Application and AI architecture", "Create C4 context, container and component views plus API and failure design.", "Target C4 and bounded AI architecture"],
    ["11", "Agentic orchestration", "Assess agent suitability, decision authority, termination, escalation and fallbacks.", "Bounded workflow; no autonomous consequential decisions"],
    ["12", "Security, guardrails and suppliers", "Threat-model access, privacy, injection, evidence integrity and supplier dependency.", "Threat model, controls, SBOM, AIBOM and exit plan"],
    ["13", "ADRs and delivery specification", "Approve requirements, NFRs, ADRs, backlog, traceability and gate conditions.", "27 requirements, 12 ADRs and G3 decision"],
]
story.append(data_table(["Stage", "Activity", "What we did", "Key evidence"], phase3, [13 * mm, 37 * mm, 69 * mm, 51 * mm], 7.1))
story.extend([
    Spacer(1, 5 * mm),
    para("C4 answer", "H2x"),
    callout("Yes. Stage 2 records the current state, Stage 10 defines target context/container/component views, and Stage 14 records the as-built architecture."),
    Spacer(1, 4 * mm),
    para("Spec-driven development answer", "H2x"),
    para("Yes. Contracts, requirements, ADRs, evaluation cases, controls and acceptance criteria were defined before the Stage 14 implementation."),
    PageBreak(),
])

# Phase 4
story.extend(heading("Stages 14-18: Build, assure and operate", "Did it work under control?"))
phase4 = [
    ["14", "Engineer and integrate", "Build the FastAPI service, browser Control Tower, evidence store, services, adapters, audit and three POCs.", "Working application and as-built architecture"],
    ["15", "Evaluate, attack and assure", "Run automated, integration, E2E, adversarial, performance and residual-risk evaluation.", "77 tests; 55 pass; 0 fail; 2 inconclusive human studies"],
    ["16", "Prepare operations and recovery", "Define SLOs, telemetry, alerts, runbooks, incidents, backup, restore, training and change control.", "Operational evidence and G5 decision"],
    ["17", "Deploy progressively", "Simulate shadow, canary, rollback and adoption evidence.", "20/20 shadow matches; 10/10 canary success"],
    ["18", "Monitor and validate resilience", "Simulate dashboards, drift, incidents, alerts and controlled-chaos recovery.", "Monitoring and resilience report"],
]
story.append(data_table(["Stage", "Activity", "What we did", "Key evidence"], phase4, [13 * mm, 37 * mm, 69 * mm, 51 * mm], 7.05))
story.extend([
    Spacer(1, 5 * mm),
    callout("Important: deployment and operation were simulated locally. This is evidence of POC control feasibility, not production history."),
    Spacer(1, 4 * mm),
    para("Stage 15 evidence location", "H2x"),
    para("docs/stages/stage_15 contains the TEVV report, red-team report, residual-risk decisions, G4 record, stage review, evaluation results, performance results and test summary."),
    PageBreak(),
])

# Phase 5
story.extend(heading("Stages 19-21: Prove, decide and close", "What was proven and what happens next?"))
phase5 = [
    ["19", "Prove value and tell the story", "Compare technical evidence with the baseline and separate measured results from hypotheses.", "Value report and executive decision story"],
    ["20", "Evaluate AIMS and lifecycle", "Audit lifecycle controls, identify gaps, create CAPAs and make the G6 decision.", "Seven open CAPAs; RESTRICT AND CHANGE"],
    ["21", "Retire and capture reusable IP", "Define retirement controls, close the academic project and retain reusable patterns.", "Closure record, lessons and reusable-IP catalog"],
]
story.append(data_table(["Stage", "Activity", "What we did", "Key evidence"], phase5, [13 * mm, 40 * mm, 68 * mm, 49 * mm], 7.35))
story.extend([
    Spacer(1, 7 * mm),
    para("What was proven", "H2x"),
])
story.append(info_cards([
    ("Control feasibility", "Evidence-backed states, explicit unknowns and human authority work on synthetic journeys."),
    ("Engineering quality", "Tests, evaluations, rollback, audit and traceability are reproducible."),
    ("Decision discipline", "Known limitations become CAPAs and restrictions, not inflated claims."),
]))
story.extend([
    Spacer(1, 7 * mm),
    para("What was not proven", "H2x"),
    para("Clinical benefit, production safety, regulatory compliance, human-factor performance, real-world savings, live integrations and live-model AI quality were not established."),
    Spacer(1, 5 * mm),
    callout("Final lifecycle decision: RESTRICT AND CHANGE", AMBER, HexColor("#C98914")),
    PageBreak(),
])

# POCs
story.extend(heading("The three proofs of concept", "What the live demo proves"))
poc_rows = [
    ["POC 1", "Identity and readiness", "Conflicting MRN and DOB evidence", "Open an owned case; authorized human applies reviewed proposal", "Identity APPLIED; readiness SATISFIED; 5 citations"],
    ["POC 2", "Safe slot orchestration", "External reservation succeeds but response times out", "Record OUTCOME_UNKNOWN; reconcile; block second dispatch", "Reconciled to SUCCEEDED; duplicate prevented"],
    ["POC 3", "Quality release", "Manufacturing, QC, deviation and thermal evidence exists without authority", "Keep release UNKNOWN until authorized Quality decision", "HUMAN AUTHORIZED; final outcome SATISFIED"],
]
story.append(data_table(
    ["POC", "Business area", "Problem", "Controlled response", "Result"],
    poc_rows,
    [14 * mm, 28 * mm, 42 * mm, 50 * mm, 36 * mm],
    6.75,
))
story.extend([
    Spacer(1, 7 * mm),
    para("The common pattern", "H2x"),
    callout("Detect uncertainty -> Preserve evidence -> Assign authority -> Apply a controlled decision -> Recalculate state -> Record audit"),
    Spacer(1, 6 * mm),
    para("What the POCs deliberately avoid", "H2x"),
    *bullets([
        "No identity is invented from a similarity score.",
        "No timeout is treated automatically as failure.",
        "No duplicate external request is sent without reconciliation.",
        "No missing Quality decision is treated as release.",
        "No AI recommendation changes authoritative state.",
    ]),
    PageBreak(),
])

# DDD C4 architecture
story.extend(heading("Architecture quick guide", "DDD, C4, contracts and ADRs"))
architecture_rows = [
    ["DDD", "Stage 5", "Defines what the business domain means", "Glossary, bounded contexts, aggregates, rules, events and state machines"],
    ["C4", "Stages 2, 10, 14", "Shows how the technical system is structured", "Current state, target context/container/component and as-built views"],
    ["Contracts", "Stage 9", "Defines stable information exchanged between parts", "Command, event-envelope and recommendation schemas"],
    ["Agent design", "Stage 11", "Defines autonomy, tools, sequencing and escalation", "Bounded deterministic orchestration with human handoff"],
    ["Threat model", "Stage 12", "Identifies how controls could fail or be abused", "Security, privacy, prompt-injection and supplier controls"],
    ["ADRs", "Stage 13", "Records why major design choices were made", "Twelve decisions with alternatives and consequences"],
]
story.append(data_table(["Method", "Stage", "Purpose", "Project evidence"], architecture_rows, [28 * mm, 29 * mm, 48 * mm, 65 * mm], 7.4))
story.extend([
    Spacer(1, 7 * mm),
    para("One-sentence relationship", "H2x"),
    callout("DDD defines the domain. C4 structures the system. Contracts define exchanges. ADRs explain choices. Tests prove behavior."),
    Spacer(1, 6 * mm),
    para("Core implementation layers", "H2x"),
])
story.append(info_cards([
    ("Interface", "Browser Control Tower, FastAPI endpoints and CLI."),
    ("Domain services", "Evidence, readiness, commands, cases, decisions and audit."),
    ("Infrastructure", "SQLite persistence and simulated external adapters."),
]))
story.append(PageBreak())

# AI boundaries
story.extend(heading("AI and human authority", "The safest answer"))
story.append(callout("The application is useful with AI off. AI is optional, non-authoritative and replaceable."))
ai_rows = [
    ["off", "Recommended default", "No model is called. Deterministic domain controls execute normally."],
    ["fake", "Bounded demonstration", "A local deterministic adapter returns a non-binding recommendation."],
    ["live", "Not supported", "No external model or provider is connected or evaluated."],
]
story.append(Spacer(1, 6 * mm))
story.append(data_table(["Mode", "Status", "Meaning"], ai_rows, [25 * mm, 45 * mm, 100 * mm], 8.0))
story.extend([
    Spacer(1, 7 * mm),
    para("AI cannot", "H2x"),
    *bullets([
        "establish patient identity or chain of identity;",
        "make clinical eligibility or readiness decisions;",
        "execute an external reservation independently;",
        "approve a deviation or product disposition; or",
        "release the product.",
    ]),
    para("Authorized humans retain", "H2x"),
    *bullets([
        "identity-resolution authority;",
        "clinical and operational exception decisions;",
        "Quality disposition and release authority; and",
        "the right to override, abstain and escalate with recorded rationale.",
    ]),
    Spacer(1, 5 * mm),
    callout("Reviewer answer: We did not add AI to create authority. We bounded AI so it can assist without becoming authority.", BLUE, TEAL),
    PageBreak(),
])

# Evidence and traceability
story.extend(heading("Evidence, traceability and assurance", "How claims are controlled"))
story.append(callout("Evidence -> Root cause -> Requirement -> ADR -> Code -> Test or evaluation -> KPI -> Lifecycle decision"))
trace_rows = [
    ["Source evidence", "Stage 2", "Frozen ZIP digest and 132 extracted-file hashes"],
    ["Problem and CTQs", "Stage 3", "Root causes, baseline and success/failure criteria"],
    ["Business rules", "Stage 5", "Eleven safety and authority rules"],
    ["Evaluation design", "Stage 7", "Fifty-seven frozen cases and thresholds"],
    ["Design decision", "Stages 9-13", "Contracts, C4, controls, requirements and ADRs"],
    ["Implementation", "Stage 14", "Source code and three integrated POCs"],
    ["Verification", "Stage 15", "Tests, TEVV, adversarial and performance evidence"],
    ["Lifecycle conclusion", "Stages 19-21", "Value boundary, CAPAs, decision and closure"],
]
story.append(Spacer(1, 5 * mm))
story.append(data_table(["Traceability element", "Stage", "Evidence"], trace_rows, [45 * mm, 28 * mm, 97 * mm], 7.7))
story.extend([
    Spacer(1, 6 * mm),
    para("Why this matters", "H2x"),
    para("A reviewer can start from a business claim and follow it to the source evidence, design decision, implementation and test. VERIFIED_INTERNAL_POC never means production validated."),
    PageBreak(),
])

# Results
story.extend(heading("What the evidence says", "Results without overclaiming"))
result_rows = [
    ["FDE stages", "21/21", "Every stage contains artifacts"],
    ["Automated tests", "77/77 passed", "Unit, integration, E2E, recovery, security and performance"],
    ["Evaluation catalog", "57 executed", "55 pass; 0 fail; 2 inconclusive human studies"],
    ["Requirements", "25/27 internal", "Two human-factor requirements need external evidence"],
    ["Shadow simulation", "20/20 matched", "AI-off and fake modes preserved domain outcomes"],
    ["Canary simulation", "10/10 succeeded", "Synthetic local journeys only"],
    ["Recovery", "Passed", "Backup, restore and AI-off rollback simulation"],
    ["Audit", "Valid", "Tamper-evident chain verified in the demo"],
]
story.append(data_table(["Measure", "Result", "Correct interpretation"], result_rows, [43 * mm, 35 * mm, 92 * mm], 8.0))
story.extend([
    Spacer(1, 7 * mm),
    para("Two inconclusive cases", "H2x"),
    para("Automation bias and safe human override require controlled participants. Software tests cannot prove how real people will respond, so the evidence correctly remains inconclusive."),
    Spacer(1, 5 * mm),
    callout("Best answer: We have strong internal technical evidence and clearly identified external evidence gaps. We do not convert gaps into passes.", MINT, TEAL),
    PageBreak(),
])

# Demo runbook
story.extend(heading("Five-minute live demo runbook", "What to say and show"))
demo_rows = [
    ["0:00", "Opening screen", "This is one controlled journey from a patient to that patient's batch."],
    ["0:30", "Four controls", "Identity is human-authorized; orchestration is idempotent; Quality retains authority; AI is off."],
    ["1:00", "Run demo", "Select AI off - recommended, then click Run demo."],
    ["1:20", "POC 1", "A conflict becomes an owned case. A human resolves identity; readiness becomes satisfied with citations."],
    ["2:10", "POC 2", "A timeout becomes unknown, is reconciled to success and is never dispatched twice."],
    ["3:00", "POC 3", "Evidence informs release, but only Quality can authorize it."],
    ["3:45", "Evidence console", "Show ten references, valid audit, deterministic mode, metrics and state digest."],
    ["4:20", "Assurance", "Show 21 stages, 77 tests, 55 of 57 evaluations and 25 of 27 requirements."],
    ["4:45", "Decision", "Close with Restrict and Change and the seven CAPAs before any real pilot."],
]
story.append(data_table(["Time", "Show", "Say"], demo_rows, [18 * mm, 43 * mm, 109 * mm], 7.75))
story.extend([
    Spacer(1, 6 * mm),
    para("Starting locally", "H2x"),
    para("Double-click START_DEMO.command, keep the Terminal open and use http://127.0.0.1:8000. The launcher creates .venv when needed and starts with AI_MODE=off."),
    Spacer(1, 4 * mm),
    callout("Do not begin the demo with code. Begin with the patient, the evidence problem and the accountable decision-maker."),
    PageBreak(),
])

# Q&A 1
story.extend(heading("Reviewer Q&A: discovery, domain and data", "Question router - part 1"))
qa1 = [
    ["What was the ask?", "1-3", "One trustworthy, evidence-backed view of identity, readiness, reservation and release."],
    ["How did you inspect the legacy estate?", "2", "Read-only forensic baseline, process/system mapping, defects, workarounds and dependencies."],
    ["Did you preserve source evidence?", "2", "Yes. The ZIP digest and all 132 frozen extraction hashes are verified."],
    ["How did you frame the problem?", "3", "SCQA, root causes, waste, KPIs, CTQs and explicit success/failure criteria."],
    ["Did you use DDD?", "5", "Yes: ubiquitous language, bounded contexts, aggregates, ownership, rules, events and state machines."],
    ["How do you handle missing data?", "5", "Missing or conflicting evidence returns UNKNOWN; it never creates automatic approval."],
    ["How do you handle late data?", "5-6", "Bitemporal evidence records both occurrence time and system-recorded time."],
    ["How did you assess data?", "6", "Quality, lineage, provenance, access, representativeness, knowledge and gap profiling."],
    ["How did you choose a source of truth?", "6", "Trust is attribute-specific; source assertions are preserved rather than globally overwritten."],
]
story.append(data_table(["Question", "Stage", "Short answer"], qa1, [55 * mm, 18 * mm, 97 * mm], 7.45))
story.append(PageBreak())

# Q&A 2
story.extend(heading("Reviewer Q&A: evaluation and architecture", "Question router - part 2"))
qa2 = [
    ["Were evaluations defined before code?", "7", "Yes. Fifty-seven cases and thresholds were frozen before Stage 14 implementation."],
    ["Did you compare options?", "8", "Yes. Six options were compared using spikes, TCO, provider/build-buy and weighted scoring."],
    ["Did you use contracts?", "9", "Yes. Commands, events and recommendations use versioned JSON schemas."],
    ["Did you use C4?", "2, 10, 14", "Yes. Current-state, target and as-built architecture views are retained."],
    ["Did you design for failure?", "10", "Yes. Timeouts, partial effects, unknown outcomes, reconciliation, compensation and fallback are explicit."],
    ["Did you use agents?", "11", "Agentic suitability was assessed, but consequential autonomy was deliberately rejected."],
    ["Did you perform threat modelling?", "12", "Yes. Access, privacy, prompt injection, evidence integrity and supplier risks were treated."],
    ["Do you have SBOM and AIBOM?", "12, 14", "Yes, as academic evidence; they are not signed production attestations."],
    ["Did you use ADRs?", "13", "Yes. Twelve ADRs record major choices, alternatives, consequences and reversibility."],
]
story.append(data_table(["Question", "Stage", "Short answer"], qa2, [55 * mm, 18 * mm, 97 * mm], 7.45))
story.append(PageBreak())

# Q&A 3
story.extend(heading("Reviewer Q&A: build, test and operations", "Question router - part 3"))
qa3 = [
    ["What did you build?", "14", "A FastAPI service, browser Control Tower, SQLite evidence store, services, adapters, audit and three POCs."],
    ["How do you prevent duplicate booking?", "5, 10, 14", "Payload-bound idempotency plus reconciliation before retry."],
    ["Did you test the solution?", "15", "Yes. All 77 tests pass; 55 evaluation cases pass; zero fail; two need human studies."],
    ["Did you red-team it?", "15", "Yes. Adversarial, injection, authority, conflict, outage, recovery and unknown-outcome cases are included."],
    ["Why are two cases inconclusive?", "15", "Automation bias and override usability require controlled human participants."],
    ["Do you have runbooks?", "16", "Yes. SLOs, alerts, incidents, change, backup, restore, rollback and training are documented."],
    ["Was it deployed?", "17", "Only as simulation: 20 shadow matches and 10 successful synthetic canary journeys."],
    ["How is it monitored?", "18", "Dashboard, SLO, alert, drift, incident and resilience-drill specifications are retained."],
]
story.append(data_table(["Question", "Stage", "Short answer"], qa3, [55 * mm, 18 * mm, 97 * mm], 7.45))
story.append(PageBreak())

# Q&A 4
story.extend(heading("Reviewer Q&A: AI, value and lifecycle", "Question router - part 4"))
qa4 = [
    ["Did you use AI?", "10-14", "AI is optional and off by default. A local fake adapter demonstrates only a bounded recommendation."],
    ["Can AI release the product?", "4, 11, 12", "No. Quality release always requires authorized human authority."],
    ["What value was proven?", "19", "Technical control feasibility: visibility, duplicate prevention, ownership and traceability."],
    ["Did you prove ROI?", "19", "No. Real savings, outcomes and production TCO were not measured."],
    ["Did you use AIMS?", "20", "An AIMS lifecycle review was performed, but no certification is claimed."],
    ["Is it production-ready?", "20", "No. The formal decision is RESTRICT AND CHANGE."],
    ["What remains?", "20", "Seven CAPAs, human studies, enterprise controls, live integrations and independent assurance."],
    ["How was the project closed?", "21", "Retirement, lessons learned, reusable IP and final closure were documented."],
]
story.append(data_table(["Question", "Stage", "Short answer"], qa4, [55 * mm, 18 * mm, 97 * mm], 7.55))
story.extend([
    Spacer(1, 7 * mm),
    callout("When challenged, do not defend an unsupported claim. Point to the stage, evidence and limitation."),
    PageBreak(),
])

# Evidence locator
story.extend(heading("Where to find the evidence", "Repository map"))
locator_rows = [
    ["Client ask and demo story", "docs/CLIENT_ASK_AND_END_TO_END_DEMO.md"],
    ["Five-minute presenter guide", "docs/DEMO_GUIDE.md"],
    ["Final capstone summary", "docs/FINAL_CAPSTONE_REPORT.md"],
    ["All 21 stage folders", "docs/stages/stage_01 through docs/stages/stage_21"],
    ["DDD artifacts", "docs/stages/stage_05"],
    ["Data and knowledge artifacts", "docs/stages/stage_06"],
    ["Evaluation design", "docs/stages/stage_07"],
    ["C4 target architecture", "docs/stages/stage_10/01_APPLICATION_AND_AI_ARCHITECTURE.md"],
    ["Security and guardrails", "docs/stages/stage_12"],
    ["ADRs and requirements", "docs/stages/stage_13 and requirements/"],
    ["As-built implementation evidence", "docs/stages/stage_14 and src/fde_capstone/"],
    ["TEVV and red-team evidence", "docs/stages/stage_15"],
    ["Operations and recovery", "docs/stages/stage_16"],
    ["Shadow/canary simulation", "docs/stages/stage_17"],
    ["Monitoring and resilience", "docs/stages/stage_18"],
    ["Value and executive story", "docs/stages/stage_19"],
    ["AIMS, CAPAs and decision", "docs/stages/stage_20"],
    ["Closure and reusable IP", "docs/stages/stage_21"],
    ["Tests", "tests/ and reports/generated/pytest-results.xml"],
    ["Final machine verification", "evidence/final_verification.json"],
]
story.append(data_table(["Need", "Location"], locator_rows, [67 * mm, 103 * mm], 7.65))
story.extend([
    Spacer(1, 6 * mm),
    para("Repository", "H2x"),
    para("github.com/86sunbot/FDE-Final-Capstone"),
    PageBreak(),
])

# Limitations and decision
story.extend(heading("The honest boundary", "What not to claim"))
story.append(info_cards([
    ("Demonstrated", "Synthetic technical control feasibility, traceability, testing, audit and recovery."),
    ("Restricted", "Real patient data, consequential AI, automated release and production integrations."),
    ("Still required", "Human studies, enterprise controls, live integration, validation and independent assurance."),
]))
story.extend([
    Spacer(1, 8 * mm),
    para("Do not say", "H2x"),
    *bullets([
        "The system is clinically validated or regulator approved.",
        "The application is production-ready.",
        "The project proved patient benefit, savings or ROI.",
        "The demo principals are enterprise IAM or electronic signatures.",
        "The external systems and decision authorities are live.",
        "A live AI model was evaluated.",
    ]),
    para("Say instead", "H2x"),
    para("The capstone demonstrates a reproducible synthetic POC with strong internal technical evidence. It identifies the external evidence and controls required before any real pilot."),
    Spacer(1, 6 * mm),
    callout("RESTRICT AND CHANGE: accept the academic POC, keep AI off, prohibit real-data use and close seven CAPAs before a new accountable gate sequence.", AMBER, HexColor("#C98914")),
    PageBreak(),
])

# Talk tracks
story.extend(heading("Ready-to-use talk tracks", "Say it simply"))
story.append(para("Thirty-second answer", "H2x"))
story.append(callout("This capstone creates one evidence-driven patient-to-batch view for Cell and Gene Therapy. It resolves identity conflicts through human authority, prevents duplicate manufacturing reservations after uncertain responses, and keeps product release with Quality. All core controls work with AI off. The synthetic POC passed 77 tests, but production use remains restricted."))
story.append(Spacer(1, 6 * mm))
story.append(para("One-minute answer", "H2x"))
story.append(para("CGT treatments in this capstone are manufactured for a specific patient, so identity, custody, timing and release must remain traceable. The current environment spreads evidence across clinical, logistics, manufacturing and Quality systems. We followed all 21 FDE stages to understand the brownfield system, model the domain and data, predefine evaluations, select a controlled architecture, build three POCs and test the result. The demo shows human-authorized identity resolution, safe reconciliation of an unknown reservation outcome and Quality-authorized release. AI is optional and off by default. The POC is technically successful, but real-data and production use remain prohibited until external evidence and seven CAPAs are completed."))
story.append(Spacer(1, 6 * mm))
story.append(para("Closing answer", "H2x"))
story.append(callout("Evidence before status. Human authority before automation. Unknown remains unknown until evidence and the correct authority resolve it.", BLUE, TEAL))
story.append(PageBreak())

# Glossary
story.extend(heading("Essential glossary", "Terms reviewers may use"))
glossary = [
    ["ADR", "Architecture Decision Record: why a major design choice was made."],
    ["AIBOM", "AI Bill of Materials: models, adapters, modes and AI dependencies."],
    ["AIMS", "AI Management System: lifecycle governance, controls, audit and improvement."],
    ["Bitemporal", "Records both when something happened and when the system learned it."],
    ["Bounded context", "A domain boundary within which terms, rules and authority are consistent."],
    ["C4", "Architecture views covering context, containers and components."],
    ["CAPA", "Corrective and Preventive Action required to close a control gap."],
    ["Chain of custody", "Traceable possession and handling of patient material or product."],
    ["Chain of identity", "Traceable link between the patient, collected material and final product."],
    ["CTQ", "Critical to Quality: a measurable condition essential to a safe result."],
    ["DDD", "Domain-Driven Design: modelling software around domain language, rules and ownership."],
    ["Idempotency", "Repeating the same command cannot create a second unintended effect."],
    ["SCQA", "Situation, Complication, Question, Answer problem-framing structure."],
    ["SBOM", "Software Bill of Materials: application software dependencies."],
    ["TEVV", "Testing, Evaluation, Verification and Validation."],
    ["UNKNOWN", "A deliberate state used when evidence cannot support satisfied or not-satisfied."],
]
story.append(data_table(["Term", "Simple meaning"], glossary, [40 * mm, 130 * mm], 7.8))
story.append(PageBreak())

# Final cheat sheet
story.extend(heading("One-page memory sheet", "Your final check before any discussion"))
memory_rows = [
    ["Client ask", "Trustworthy identity, readiness, reservation, release and evidence"],
    ["Problem", "Fragmented evidence, unsafe assumptions, duplicate effects and unclear authority"],
    ["Solution", "Evidence-driven Control Tower with explicit unknowns and owned exceptions"],
    ["POC 1", "Human-authorized identity resolution and readiness"],
    ["POC 2", "Unknown-outcome reconciliation and duplicate prevention"],
    ["POC 3", "Quality-authorized product release"],
    ["DDD", "Stage 5"],
    ["C4", "Stages 2, 10 and 14"],
    ["Evaluations", "Stage 7 defines; Stage 15 executes"],
    ["Security", "Stage 12 designs; Stage 15 tests"],
    ["Implementation", "Stage 14"],
    ["Operations", "Stages 16-18"],
    ["Value", "Stage 19 - technical feasibility, not ROI"],
    ["Decision", "Stage 20 - RESTRICT AND CHANGE"],
    ["Closure", "Stage 21"],
    ["Evidence", "21 stages; 77 tests; 55/57 pass; 25/27 internal requirements"],
    ["AI", "Optional, off by default and never authoritative"],
    ["Boundary", "Synthetic academic POC; not clinical, regulatory or production validation"],
]
story.append(data_table(["Topic", "Answer"], memory_rows, [45 * mm, 125 * mm], 8.0))
story.extend([
    Spacer(1, 7 * mm),
    callout("UNDERSTAND -> MODEL -> DESIGN -> PROVE -> DECIDE", MINT, TEAL),
    Spacer(1, 6 * mm),
    Paragraph("Surya's final sentence", styles["H2x"]),
    Paragraph(
        "We built a controlled, evidence-driven CGT patient-to-batch POC that preserves human authority, manages uncertainty and proves its internal technical behavior without claiming production readiness.",
        ParagraphStyle(name="final-quote", parent=styles["Callout"], fontSize=12, leading=18, textColor=TEAL, alignment=TA_CENTER),
    ),
])


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=20 * mm,
    leftMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=20 * mm,
    title="Surya's FDE Capstone Bible",
    author="Surya - FDE Final Capstone",
    subject="CGT Patient-to-Batch Orchestration executive reference and question guide",
    creator="Codex",
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(OUTPUT)
