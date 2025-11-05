from fastapi import APIRouter, Depends
from typing import List
from schemas import Patient
from db import get_conn
from auth import get_current_role

router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.post("", response_model=Patient)
def create_patient(p: Patient, role: str = Depends(get_current_role)):
    if role not in ("doctor","nurse"):
        raise Exception("forbidden")
    conn = get_conn()
    cur = conn.execute("INSERT INTO patients(name,age,sensitivity) VALUES(?,?,?)", (p.name, p.age, p.sensitivity))
    p.id = cur.lastrowid
    conn.commit(); conn.close()
    return p

@router.get("", response_model=List[Patient])
def list_patients(role: str = Depends(get_current_role)):
    conn = get_conn()
    rows = conn.execute("SELECT id,name,age,sensitivity FROM patients").fetchall()
    conn.close()
    return [Patient(id=r["id"], name=r["name"], age=r["age"], sensitivity=r["sensitivity"]) for r in rows]
