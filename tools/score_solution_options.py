#!/usr/bin/env python3
"""Validate and score the Stage 8 option matrix."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/stages/stage_08/option_scores.json"
OUTPUT = ROOT / "docs/stages/stage_08/option_scores.csv"


def calculate() -> list[dict]:
    document = json.loads(SOURCE.read_text(encoding="utf-8"))
    criteria = document["criteria"]
    weights = {item["id"]: item["weight"] for item in criteria}
    if sum(weights.values()) != 100:
        raise ValueError("Criterion weights must total 100")
    if len(weights) != len(criteria):
        raise ValueError("Criterion IDs must be unique")

    rows = []
    for option in document["options"]:
        if set(option["scores"]) != set(weights):
            raise ValueError(f'{option["id"]}: score keys do not match criteria')
        if any(not isinstance(score, int) or score < 1 or score > 5 for score in option["scores"].values()):
            raise ValueError(f'{option["id"]}: scores must be integers from 1 to 5')
        weighted = sum(option["scores"][key] * weight for key, weight in weights.items()) / 100
        rows.append(
            {
                "option_id": option["id"],
                "name": option["name"],
                "weighted_score": f"{weighted:.2f}",
                "safety_threshold": option["safety_threshold"],
                "decision": option["decision"],
            }
        )
    if [row["option_id"] for row in rows if row["decision"] == "RECOMMEND"] != ["O3"]:
        raise ValueError("Exactly O3 must be the documented recommendation")
    return sorted(rows, key=lambda row: float(row["weighted_score"]), reverse=True)


def main() -> None:
    rows = calculate()
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
