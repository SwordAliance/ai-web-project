from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.prediction import PredictRequest, PredictResponse
from app.tasks.predict_tasks import generate_prediction

router = APIRouter(tags=["predict"])


@router.post("/predict", response_model=PredictResponse, status_code=status.HTTP_202_ACCEPTED)
def predict(payload: PredictRequest) -> PredictResponse:
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Пустой prompt недопустим")

    task = generate_prediction.delay(payload.prompt, payload.creativity)
    return PredictResponse(task_id=task.id)
