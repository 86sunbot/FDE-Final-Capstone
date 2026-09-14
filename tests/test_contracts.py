import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_machine_readable_contracts_are_strict_and_versioned():
    for name in ["event-envelope", "command", "recommendation"]:
        contract = json.loads((ROOT / f"stage_09/contracts/{name}.schema.json").read_text(encoding="utf-8"))
        assert contract["$schema"].endswith("2020-12/schema")
        assert contract["additionalProperties"] is False
        assert contract["required"]


def test_recommendation_contract_has_no_authority_or_execution_fields():
    contract = json.loads((ROOT / "stage_09/contracts/recommendation.schema.json").read_text(encoding="utf-8"))
    assert set(contract["properties"]) == {"summary", "evidence_refs", "uncertainty", "next_actions"}
