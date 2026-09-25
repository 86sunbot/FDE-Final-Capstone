# Repository organization and evidence boundaries

## Assessment

The capstone's essential paths are coherent: `src/` contains the runnable application; `tests/` and `tools/` contain verification; `requirements/`, `docs/stages/` and `participant_artifacts/` hold the 21-stage evidence. The frozen `source_baseline/` remains separate and unchanged.

The previous root mixed those essential paths with presentation media, a framework PDF and historical exports. Tracked PDF render previews were also under `tmp/`, which made temporary work look current. The organization below moves these materials without deleting them.

## Current structure

| Path | Role | Keep current? |
|---|---|---|
| [`src/`](../src) | App, API, domain services and browser UI | Yes |
| [`tests/`](../tests), [`tools/`](../tools) | Tests and reproducible checks | Yes |
| [`requirements/`](../requirements), [`evidence/`](../evidence), [`reports/`](../reports) | Traceability and generated verification evidence | Yes |
| [`docs/stages/`](stages), [`participant_artifacts/`](../participant_artifacts) | Canonical stage record and participant-facing 21-stage submission | Yes; keep both views |
| [`source_baseline/`](../source_baseline) | Frozen challenge evidence | Yes; immutable |
| [`presentation/`](../presentation) | Current deck, scripts, talk tracks and media | Yes |
| [`reference/`](../reference) | Supplied operating-model framework | Yes |
| [`output/pdf/`](../output/pdf) | Personal study-guide PDF | Optional output |
| [`archive/`](../archive) | Historical assessments, drafts and intermediate renders | Archived |

`docs/stages/` and `participant_artifacts/` are intentionally separate: the former holds the detailed engineering record; the latter is the participant-facing 21-stage hand-in. They are related through the [185-row artifact register](21_STAGE_ARTIFACT_REGISTER.md), so collapsing or renaming either tree would break evidence links.

## Navigation and maintenance rules

- The root [README](../README.md) is the landing page. It links directly to the submission, stage evidence, app, tests, presentation, frozen baseline and archive so these folders remain reachable in GitHub Mobile.
- [The documentation hub](README.md) is the index for reports and decisions. [The participant index](../participant_artifacts/README.md) is the index for the 21-stage hand-in. [The presentation index](../presentation/README.md) identifies the current talk track and media.
- Keep the supplied `source_baseline/` unchanged. Add derived analysis under `docs/`, `requirements/`, `tools/` or `evidence/` with a source reference and explicit scope.
- Keep a historical result tied to the report that produced it. A later test rerun does not silently rewrite an earlier Stage 15 result or turn an internal check into independent assurance.
- Put superseded drafts in `archive/` and keep current presenter-facing material linked from the landing page. Before moving any canonical file, update the artifact register and links that depend on its path.
- Production claims require the owner approvals and gates recorded in Stage 20. The completed academic capstone remains `RESTRICT_AND_CHANGE` for real-world use.

## Archive decision

- Moved earlier assessments, the previous 10-slide PDF and the obsolete video-transcript draft to `archive/`.
- Moved tracked PDF render previews from `tmp/pdfs/` to `archive/pdf-build/`. The finished study guide remains in `output/pdf/`.
- Moved the active video, captions and slide frames into `presentation/media/`, and updated the deck generator and demo guides to use their new locations.
- Moved the operating-model PDF to `reference/` because the stage register still needs it.

No capstone artifact, source baseline file, application module, test or requirement was removed. The archived paths remain recoverable through Git history.

## Remaining content risk

The existing PowerPoint deck has a stale closing speaker note that overstates this synthetic academic POC as a complete, mathematically verified GxP platform. It also refers to the video's former root-level path. The [speaker guide](../presentation/SPEAKER_SCRIPT_AND_TIMING_GUIDE_40MIN.md) and [generator](../presentation/generate_presentation.py) now use the correct boundary and media paths, but the committed deck itself has not been regenerated in this repository-organization pass. Regenerate and review it before presenting. Its other claims should receive a separate factual review against the current evidence register.
