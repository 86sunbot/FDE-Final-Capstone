def test_audit_chain_verifies_and_detects_tampering(app):
    app.db.audit("A", "read", "J-1", "ALLOWED", {"x": 1}, "T-1")
    app.db.audit("B", "write", "J-1", "DENIED", {"reason": "test"}, "T-2")
    assert app.db.verify_audit_chain() is True
    app.db.connection.execute("UPDATE audit SET outcome='ALTERED' WHERE audit_id=1")
    assert app.db.verify_audit_chain() is False
