#!/usr/bin/env python3
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    xml_path = ROOT / "reports/generated/pytest-results.xml"
    root = ET.parse(xml_path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    totals = {key: sum(int(float(suite.attrib.get(key, 0))) for suite in suites) for key in ["tests", "failures", "errors", "skipped"]}
    total_time = sum(float(suite.attrib.get("time", 0)) for suite in suites)
    report = {
        "scope": "clean capstone automated pytest suite",
        **totals,
        "passed": totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"],
        "time_seconds": round(total_time, 6),
        "junit_evidence": "reports/generated/pytest-results.xml",
    }
    output = ROOT / "stage_15/test_summary.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
