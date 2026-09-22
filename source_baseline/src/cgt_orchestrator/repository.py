import sqlite3
from .paths import db_path

class LegacyRepository:
    def __init__(self, path=None):
        self.path = str(path or db_path())

    def _rows(self, sql, args=()):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        try:
            return [dict(r) for r in con.execute(sql, args).fetchall()]
        finally:
            con.close()

    def patient(self, patient_key: str):
        rows = self._rows("SELECT * FROM patients WHERE patient_key=?", (patient_key,))
        return rows[0] if rows else None

    def journey(self, patient_key: str):
        return {
            "patient": self.patient(patient_key),
            "collections": self._rows("SELECT * FROM collections WHERE patient_key=?", (patient_key,)),
            "shipments": self._rows("SELECT * FROM shipments WHERE patient_key=? ORDER BY departed_at", (patient_key,)),
            "batches": self._rows("SELECT * FROM batches WHERE patient_key=?", (patient_key,)),
            "slots": self._rows("SELECT * FROM manufacturing_slots WHERE patient_key=?", (patient_key,)),
            "consents": self._rows("SELECT * FROM consents WHERE patient_key=?", (patient_key,)),
            "authorizations": self._rows("SELECT * FROM insurance_authorizations WHERE patient_key=?", (patient_key,)),
        }

    def open_deviations(self):
        return self._rows("SELECT * FROM deviations WHERE status <> 'CLOSED'")
