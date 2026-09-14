import json
from pathlib import Path

from tools.score_solution_options import calculate


ROOT = Path(__file__).resolve().parents[1]


def test_option_weights_total_one_hundred_and_scores_are_bounded():
    document = json.loads((ROOT / "docs/stages/stage_08/option_scores.json").read_text(encoding="utf-8"))
    assert sum(item["weight"] for item in document["criteria"]) == 100
    assert all(1 <= value <= 5 for option in document["options"] for value in option["scores"].values())


def test_o3_is_recommended_and_has_best_score_among_safe_capstone_options():
    rows = calculate()
    selected = next(row for row in rows if row["decision"] == "RECOMMEND")
    assert selected["option_id"] == "O3"
    eligible = [row for row in rows if row["safety_threshold"] == "PASS_HYPOTHESIS"]
    assert float(selected["weighted_score"]) == max(float(row["weighted_score"]) for row in eligible)


def test_an_option_cannot_win_on_weighted_score_after_failing_safety():
    rows = calculate()
    assert all(row["decision"] != "RECOMMEND" for row in rows if row["safety_threshold"] != "PASS_HYPOTHESIS")
