from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdapterResult:
    kind: str
    reservation_id: str | None = None
    detail: str | None = None


class SlotSimulator:
    """Deterministic external-system substitute used only by the academic POC."""

    def reserve(self, command_id: str, patient_key: str, slot_id: str, behavior: str = "success") -> AdapterResult:
        reservation_id = f"RSV-{command_id}"
        if behavior == "success":
            return AdapterResult("SUCCESS", reservation_id)
        if behavior == "timeout_after_success":
            return AdapterResult("TIMEOUT_AFTER_SUCCESS", reservation_id)
        if behavior == "partial":
            return AdapterResult("PARTIAL", reservation_id)
        if behavior == "failure":
            return AdapterResult("FAILURE", None, "SIMULATED_EXPLICIT_FAILURE")
        raise ValueError("UNKNOWN_SIMULATOR_BEHAVIOR")
