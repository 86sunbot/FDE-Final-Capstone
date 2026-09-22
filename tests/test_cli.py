from __future__ import annotations

import json
import sys

import pytest

from fde_capstone.cli import main


def invoke(monkeypatch, capsys, *arguments: str) -> dict:
    monkeypatch.setattr(sys, "argv", ["fde-capstone", *arguments])
    main()
    return json.loads(capsys.readouterr().out)


def test_cli_init_and_backup(monkeypatch, capsys, tmp_path):
    database = tmp_path / "capstone.db"
    initialized = invoke(monkeypatch, capsys, "init", "--db", str(database))
    assert initialized == {"status": "initialized", "db": str(database)}
    assert database.is_file()

    destination = tmp_path / "backup.db"
    backed_up = invoke(
        monkeypatch,
        capsys,
        "backup",
        "--db",
        str(database),
        "--output",
        str(destination),
    )
    assert backed_up["status"] == "backed_up"
    assert backed_up["path"] == str(destination)
    assert len(backed_up["source_state_digest"]) == 64
    assert destination.is_file()


def test_cli_demo(monkeypatch, capsys, tmp_path):
    result = invoke(
        monkeypatch,
        capsys,
        "demo",
        "--db",
        str(tmp_path / "demo.db"),
        "--ai-mode",
        "off",
    )
    assert result["scope"] == "SYNTHETIC_LOCAL_ACADEMIC_POC"
    assert result["poc1"]["readiness"] == "SATISFIED"
    assert result["poc2"]["reconciled_state"] == "SUCCEEDED"
    assert result["poc3"]["released"] is True


def test_cli_evaluate(monkeypatch, capsys, tmp_path):
    output = tmp_path / "evaluation.json"
    result = invoke(
        monkeypatch,
        capsys,
        "evaluate",
        "--db",
        str(tmp_path / "unused.db"),
        "--output",
        str(output),
    )
    assert result["catalog_cases"] == 57
    assert result["executed"] == 57
    assert result["fail"] == 0
    assert output.is_file()


def test_cli_invalid_command_exits_nonzero(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["fde-capstone", "unknown"])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
