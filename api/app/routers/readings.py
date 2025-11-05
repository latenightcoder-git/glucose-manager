from fastapi import APIRouter, Depends
from schemas import Reading
from db import get_conn
from auth import get_current_role

router = APIRouter(prefix="/api/readings", tags=["readings"])

@router.post("")
def add_reading(r: Reading, role: str = Depends(get_current_role)):
    conn = get_conn()
    conn.execute("INSERT INTO readings(patient_id,glucose,insulin,carbs,activity,note) VALUES(?,?,?,?,?,?)",
                    (r.patient_id, r.glucose, r.insulin, r.carbs, r.activity, r.note))
    conn.commit(); conn.close()
    return {"ok": True}

@router.get("/{patient_id}")
def get_readings(patient_id: int, role: str = Depends(get_current_role)):
    conn = get_conn()
    rows = conn.execute("SELECT id,glucose,insulin,carbs,activity,ts FROM readings WHERE patient_id=? ORDER BY ts ASC",
                        (patient_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
