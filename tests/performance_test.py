import statistics
import time

from fde_capstone.model import Outcome


def test_deterministic_projection_p95_is_below_local_poc_threshold(app, principals, evidence):
    mapping = {"identity": "EV-ID", "consent": "EV-CONSENT", "authorization": "EV-AUTH", "site": "EV-SITE"}
    for item in mapping.values():
        evidence(item)
    prerequisites = {name: (Outcome.SATISFIED, [item]) for name, item in mapping.items()}
    samples = []
    for _ in range(1000):
        started = time.perf_counter()
        result = app.readiness.assess(principals["viewer"], "J-1", "PRE_COLLECTION", prerequisites)
        samples.append((time.perf_counter() - started) * 1000)
    assert result.outcome == Outcome.SATISFIED
    assert statistics.quantiles(samples, n=100)[94] <= 250
