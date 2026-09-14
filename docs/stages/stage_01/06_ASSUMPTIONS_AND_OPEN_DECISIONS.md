# Stage 1 - Assumptions, Constraints and Open Decisions

**Status:** Active  
**Last updated:** 2026-09-14

## Assumptions

| ID | Assumption | Basis | Risk if wrong | Validation owner/status |
|---|---|---|---|---|
| A-001 | The user is the Capstone Owner and may approve academic/project artifacts | User initiated and directed the work | Stage approvals may lack a clear owner | User confirmation pending |
| A-002 | The original ZIP is the authoritative immutable challenge package | User-provided file and verified manifest | Wrong baseline would invalidate findings | Verified technically; user confirmation pending |
| A-003 | All challenge data is synthetic and may be processed locally | Package README and licence reference | Privacy or usage restriction | Licence review in Stage 4 |
| A-004 | The capstone target is a locally runnable POC, not production deployment | Challenge framing and user request | Over- or under-engineering | Confirm in Stage 1 review |
| A-005 | Cloud AI is optional and disabled by default | Challenge AGENTS.md | Live-model expectations may differ | Confirm before Stage 8 selection |
| A-006 | Role-based stakeholder placeholders are acceptable until named reviewers are available | Synthetic challenge has no organization roster | Cannot claim actual stakeholder engagement | Names or academic-role approval pending |
| A-007 | Eight weeks is a planning model, not a committed deadline | Master plan proposal | Sequence may need compression | User deadline pending |
| A-008 | The existing AntiGravity repository may be mined selectively but not treated as the final base without validation | Prior independent audit | Rework or inherited defects | Component disposition in Stage 2/8 |

## Constraints

| ID | Constraint | Source |
|---|---|---|
| C-001 | Preserve original evidence and intentional inconsistencies | Challenge AGENTS.md and user instruction |
| C-002 | No autonomous consequential decisions | Challenge AGENTS.md and FDE framework |
| C-003 | Add tests before correcting intentional defects | Challenge AGENTS.md |
| C-004 | Local-first baseline without cloud credentials | Challenge AGENTS.md |
| C-005 | Separate deterministic and AI-assisted components | Challenge brief/AGENTS.md |
| C-006 | Produce all ten challenge deliverables through the 21-stage model | Challenge brief and FDE framework |
| C-007 | Use Codex as the engineering environment henceforth | User decision |

## Open decisions

| ID | Decision required | Why it matters | Recommended default | Needed by |
|---|---|---|---|---:|
| Q-001 | Confirm the Capstone Owner and approval method | Required to mark stages approved | User acts as Capstone Owner; written approval in task | Stage 1 exit |
| Q-002 | Confirm final assessment audience | Controls depth and presentation style | Senior FDE architecture panel plus business sponsor | Stage 3 |
| Q-003 | Confirm submission deadline | Determines sequencing and scope of optional work | Eight-week plan, compressible by gate | Stage 3 |
| Q-004 | Confirm expected final formats | Determines artifact backlog | Git repository, Markdown evidence pack, runnable demo and executive presentation | Stage 8 |
| Q-005 | Confirm whether a live Gemini/OpenAI model demonstration is required | Affects provider assessment, keys and evaluation | Keep optional adapter; primary demo runs in deterministic/mock mode | Stage 8 |
| Q-006 | Confirm who can act as independent reviewer | Needed before claiming independent assurance | External human reviewer or explicitly label internal assurance only | Stage 15 |
| Q-007 | Confirm whether the AntiGravity GitHub repository is the target delivery repository | Affects branching and cleanup strategy | Build in a clean Codex-controlled project, then migrate approved assets | Before Stage 14 |

## Current decisions

| ID | Decision | Status | Rationale |
|---|---|---|---|
| D-001 | Use Codex for future capstone implementation | Accepted by user | Establishes one engineering workflow |
| D-002 | Keep the original ZIP unchanged | Accepted by user and technically verified | Preserves evidence integrity |
| D-003 | Treat AntiGravity output as prior prototype evidence | Accepted working decision | Prevents inherited claims from becoming assumed truth |
| D-004 | Track completion by evidence-backed exit gates | Accepted working decision | Avoids artifact-count completion theater |
