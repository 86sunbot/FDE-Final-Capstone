import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/21_STAGE_ARTIFACT_REGISTER.csv"


def test_each_pdf_essential_artifact_has_a_unique_canonical_row_and_valid_path():
    with REGISTER.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 185
    assert len({row["artifact_id"] for row in rows}) == len(rows)
    assert {row["stage"] for row in rows} == {f"{stage:02}" for stage in range(1, 22)}
    assert Counter(row["status"] for row in rows) == {
        "PRESENT_INTERNAL": 88,
        "PARTIAL": 72,
        "CONDITIONAL_NOT_SELECTED": 16,
        "EXTERNAL_REQUIRED": 9,
    }
    for row in rows:
        path = row["canonical_path"]
        if path == "-":
            assert row["status"] in {"MISSING", "EXTERNAL_REQUIRED", "CONDITIONAL_NOT_SELECTED"}
        else:
            assert (ROOT / path).is_file(), row["artifact_id"]
        assert row["accountable_role"] and row["exit_evidence"]


def test_prd_is_identified_as_a_training_extra_not_a_pdf_essential_artifact():
    with REGISTER.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    extras = [row for row in rows if "-X" in row["artifact_id"]]
    assert len(extras) == 1
    assert extras[0]["artifact_id"] == "S13-X01"
    assert "PRODUCT_REQUIREMENTS_DOCUMENT" in extras[0]["canonical_path"]
