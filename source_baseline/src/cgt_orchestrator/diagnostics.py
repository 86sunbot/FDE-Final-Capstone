from collections import Counter
from datetime import datetime
from .repository import LegacyRepository


def run_diagnostics(repo=None):
    repo = repo or LegacyRepository()
    con_path = repo.path
    import sqlite3
    con = sqlite3.connect(con_path); con.row_factory = sqlite3.Row
    out = {}
    try:
        patients=[dict(r) for r in con.execute("select * from patients")]
        shipments=[dict(r) for r in con.execute("select * from shipments")]
        batches=[dict(r) for r in con.execute("select * from batches")]
        slots=[dict(r) for r in con.execute("select * from manufacturing_slots")]
        consents=[dict(r) for r in con.execute("select * from consents")]
        quals=[dict(r) for r in con.execute("select * from site_qualifications")]
        mrns=Counter(p['mrn'] for p in patients)
        out['patient_count']=len(patients)
        out['duplicate_mrn_count']=sum(1 for _,n in mrns.items() if n>1)
        out['impossible_shipment_time_count']=sum(1 for s in shipments if s['arrived_at'] and s['departed_at'] and s['arrived_at'] < s['departed_at'])
        out['mes_qms_conflict_count']=sum(1 for b in batches if b['mes_status']=='RELEASED' and b['qms_release_status']!='RELEASED')
        out['slot_state_conflict_count']=sum(1 for s in slots if s['scheduler_state']=='CONFIRMED' and s['mes_state']=='CANCELLED')
        out['withdrawn_consent_count']=sum(1 for c in consents if c['status']=='WITHDRAWN')
        out['expired_or_due_site_controls']=sum(1 for q in quals if q['training_status']=='EXPIRED' or q['equipment_status']=='DUE')
    finally:
        con.close()
    return out
