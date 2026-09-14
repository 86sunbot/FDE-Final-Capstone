from fde_capstone.demo import run_demo


def test_three_pocs_share_one_controlled_runtime(tmp_path):
    result = run_demo(tmp_path / "demo.db", ai_mode="off")
    assert result["poc1"]["decision"] == "APPLIED"
    assert result["poc1"]["readiness"] == "SATISFIED"
    assert result["poc2"] == {"initial_state": "OUTCOME_UNKNOWN", "reconciled_state": "SUCCEEDED", "replay_dispatch": False}
    assert result["poc3"]["released"] is True
    assert result["assistant"] == {"mode": "DETERMINISTIC_ONLY", "rejection_reason": "AI_DISABLED"}
    assert result["audit_chain_valid"] is True


def test_bounded_fake_assistant_never_becomes_authority(tmp_path):
    result = run_demo(tmp_path / "demo-ai.db", ai_mode="fake")
    assert result["assistant"]["mode"] == "BOUNDED_AI"
    assert result["poc3"]["released"] is True
    assert result["audit_chain_valid"] is True
