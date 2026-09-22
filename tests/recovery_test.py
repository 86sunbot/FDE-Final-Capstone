from fde_capstone.application import CapstoneApplication
from fde_capstone.demo import run_demo


def test_backup_restore_preserves_state_digest(tmp_path):
    source = tmp_path / "source.db"
    run_demo(source)
    app = CapstoneApplication(source)
    before = app.db.state_digest()
    backup = app.db.backup(tmp_path / "backup.db")
    app.close()
    restored = CapstoneApplication(backup)
    after = restored.db.state_digest()
    assert before == after
    assert restored.db.verify_audit_chain() is True
    restored.close()
