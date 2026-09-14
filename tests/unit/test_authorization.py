import pytest

from fde_capstone.model import Principal
from fde_capstone.security import AuthorizationError, decide


def test_body_claim_cannot_expand_server_principal_role(app, principals):
    payload = {"role": "QUALITY_AUTHORITY", "batch_id": "B-1"}
    with pytest.raises(AuthorizationError):
        app.quality.authorize_release(principals["viewer"], payload["batch_id"], "EV-MISSING")
    assert app.db.metrics()["authorization_denied"]["count"] == 1


def test_cross_scope_access_is_denied(principals):
    result = decide(principals["limited"], "read", "J-DENIED")
    assert result.allowed is False
    assert result.reason == "SCOPE_DENIED"


def test_missing_principal_is_denied():
    assert decide(None, "read", "J-1").reason == "MISSING_PRINCIPAL"
