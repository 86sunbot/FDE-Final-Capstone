import pytest

from fde_capstone.application import CapstoneApplication
from fde_capstone.model import Principal


@pytest.fixture
def app():
    service = CapstoneApplication(":memory:")
    yield service
    service.close()


@pytest.fixture
def principals():
    return {
        "coordinator": Principal("coordinator", frozenset({"COORDINATOR"}), frozenset({"*"})),
        "identity": Principal("identity", frozenset({"IDENTITY_AUTHORITY"}), frozenset({"*"})),
        "planner": Principal("planner", frozenset({"PLANNER"}), frozenset({"*"})),
        "quality": Principal("quality", frozenset({"QUALITY_AUTHORITY"}), frozenset({"*"})),
        "viewer": Principal("viewer", frozenset({"VIEWER"}), frozenset({"*"})),
        "limited": Principal("limited", frozenset({"VIEWER"}), frozenset({"J-ALLOWED"})),
    }


@pytest.fixture
def evidence(app):
    def add(evidence_id, source="TEST", payload=None, occurred="2026-01-01T00:00:00+00:00", recorded=None):
        return app.evidence.register(evidence_id, source, f"test://{evidence_id}", payload or {"id": evidence_id}, occurred, recorded or occurred)
    return add
