from fastapi import APIRouter, Depends
import numpy as np
from schemas import RecommendationRequest, RecommendationResponse
from auth import get_current_role

router = APIRouter(prefix="/api", tags=["recommendation"])

MODEL = {"agent": None}

def fuzzy_guardrails(glucose, activity, exercising):
    if glucose >= 180 and (activity >= 0.5 or exercising):
        return True, "High glucose but exercising; defer insulin"
    if glucose < 80:
        return True, "Hypoglycemia risk; no insulin; consider carbs"
    return False, ""

@router.post("/recommend", response_model=RecommendationResponse)
def recommend(req: RecommendationRequest, role: str = Depends(get_current_role)):
    blocked, reason = fuzzy_guardrails(req.glucose, req.activity, req.exercising)
    if blocked:
        return RecommendationResponse(action_units=0.0, reason=reason)
    agent = MODEL.get("agent")
    if agent is None:
        delta = req.glucose - 120.0
        u = max(0.0, min(6.0, delta/50.0))
        return RecommendationResponse(action_units=float(u), reason="Heuristic (model warming up)")
    obs = np.array([req.glucose, req.insulin_on_board, req.carbs, req.activity], dtype=np.float32)
    act = agent.select_action(obs, noise_std=0.0, deterministic=True)
    return RecommendationResponse(action_units=float(act[0]), reason="RL policy")
