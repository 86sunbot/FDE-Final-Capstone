#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fde_capstone.demo import run_demo


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="fde-deploy-") as temp:
        directory = Path(temp)
        shadow = []
        for index in range(20):
            off = run_demo(directory / f"shadow-off-{index}.db", "off")
            fake = run_demo(directory / f"shadow-fake-{index}.db", "fake")
            same_domain_outcome = off["poc1"]["readiness"] == fake["poc1"]["readiness"] and off["poc2"] == fake["poc2"] and off["poc3"]["released"] == fake["poc3"]["released"]
            shadow.append(same_domain_outcome)
        canary = [run_demo(directory / f"canary-{index}.db", "off") for index in range(10)]
        rollback = run_demo(directory / "rollback-ai-off.db", "off")
    report = {
        "scope": "local synthetic deployment simulation only",
        "release_mode": "AI off",
        "shadow_runs": len(shadow),
        "shadow_domain_matches": sum(shadow),
        "canary_runs": len(canary),
        "canary_success": sum(1 for result in canary if result["audit_chain_valid"] and result["poc3"]["released"]),
        "rollback": {"from": "fake assistant enabled", "to": "AI off", "deterministic_service_available": rollback["assistant"]["mode"] == "DETERMINISTIC_ONLY"},
        "production_deployment": False,
        "pass": all(shadow) and all(result["audit_chain_valid"] for result in canary) and rollback["assistant"]["mode"] == "DETERMINISTIC_ONLY",
    }
    output = ROOT / "docs/stages/stage_17/deployment_simulation_results.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
