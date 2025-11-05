from pydantic import BaseModel
from typing import Optional, List

class Login(BaseModel):
    username: str
    password: str

class Patient(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    sensitivity: float = 1.0

class Reading(BaseModel):
    patient_id: int
    glucose: float
    insulin: float
    carbs: float = 0.0
    activity: float = 0.0
    note: Optional[str] = None

class RecommendationRequest(BaseModel):
    patient_id: int
    glucose: float
    insulin_on_board: float
    carbs: float
    activity: float
    exercising: bool = False

class RecommendationResponse(BaseModel):
    action_units: float
    reason: str
