import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_assistant_registry_matches_allowed_runtime_modes_and_has_no_live_provider():
    config = json.loads((ROOT / "docs/stages/stage_14/assistant_config_registry.json").read_text())
    assert config["default_mode"] == "off"
    assert set(config["approved_modes"]) == {"off", "fake"}
    assert all(not mode["production_provider"] for mode in config["approved_modes"].values())
    assert "live-provider" in config["unselected"]
