#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with (ROOT / "requirements/requirements.csv").open(newline="", encoding="utf-8") as handle:
        requirements = list(csv.DictReader(handle))
    rows = []
    for requirement in requirements:
        human = requirement["requirement_id"].startswith("REQ-HUM-")
        status = "INCONCLUSIVE_EXTERNAL_EVIDENCE_REQUIRED" if human else "VERIFIED_INTERNAL_POC"
        evidence = requirement["test_reference"] if human else f'{requirement["test_reference"]}; docs/stages/stage_15/test_summary.json'
        rows.append(requirement | {"verification_status": status, "verification_evidence": evidence})
    output_csv = ROOT / "requirements/verification_matrix.csv"
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "total": len(rows),
        "verified_internal_poc": sum(row["verification_status"] == "VERIFIED_INTERNAL_POC" for row in rows),
        "inconclusive_external_evidence_required": sum(row["verification_status"] == "INCONCLUSIVE_EXTERNAL_EVIDENCE_REQUIRED" for row in rows),
        "production_verified": 0,
    }
    (ROOT / "requirements/verification_matrix.json").write_text(json.dumps({"summary": summary, "requirements": rows}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
