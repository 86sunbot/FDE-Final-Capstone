#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    baseline = json.loads((ROOT / "docs/stages/stage_03/kpi_baseline.json").read_text(encoding="utf-8"))
    evaluation = json.loads((ROOT / "docs/stages/stage_15/evaluation_results.json").read_text(encoding="utf-8"))
    performance = json.loads((ROOT / "docs/stages/stage_15/performance_results.json").read_text(encoding="utf-8"))
    deployment = json.loads((ROOT / "docs/stages/stage_17/deployment_simulation_results.json").read_text(encoding="utf-8"))
    report = {
        "scope": "synthetic academic evidence; not real-world benefit or ROI",
        "baseline": baseline["summary"],
        "measured_capstone": {
            "evaluation_pass": evaluation["summary"]["pass"],
            "evaluation_fail": evaluation["summary"]["fail"],
            "evaluation_inconclusive": evaluation["summary"]["inconclusive"],
            "deterministic_projection_p95_ms": performance["p95_ms"],
            "shadow_domain_matches": deployment["shadow_domain_matches"],
            "shadow_runs": deployment["shadow_runs"],
            "canary_success": deployment["canary_success"],
            "canary_runs": deployment["canary_runs"]
        },
        "not_measured": [
            "real vein-to-vein time", "real avoidable delay", "real on-time infusion", "real labor savings",
            "real user adoption or workload", "human-factor benefit", "live-model quality/cost", "production TCO or ROI"
        ],
        "ai_increment_decision": "NOT PROVEN; keep AI off until controlled human and live-model comparison passes",
        "claim_decision": "The POC demonstrates deterministic safety/control feasibility on synthetic cases; it does not demonstrate clinical, operational, regulatory or financial outcomes."
    }
    output = ROOT / "docs/stages/stage_19/value_report.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
