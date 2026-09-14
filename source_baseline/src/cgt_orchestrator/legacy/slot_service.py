"""Legacy slot reservation with intentionally weak idempotency semantics."""
import uuid

class SlotService:
    def __init__(self):
        self.reservations = []

    def reserve(self, patient_key: str, site_id: str):
        # Defect: every retry creates a new reservation identifier.
        reservation = {"reservation_id": str(uuid.uuid4()), "patient_key": patient_key, "site_id": site_id, "status": "RESERVED"}
        self.reservations.append(reservation)
        return reservation
