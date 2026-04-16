from __future__ import annotations

from fastapi import APIRouter

from app.schemas.prediction import HealthResponse
from app.services.health_service import check_database, check_redis, check_model

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    db_ok = False
    redis_ok = False
    model_ok = False

    try:
        db_ok = check_database()
    except Exception:
        db_ok = False

    try:
        redis_ok = check_redis()
    except Exception:
        redis_ok = False

    try:
        model_ok = check_model()
    except Exception:
        model_ok = False

    overall = "ok" if db_ok and redis_ok and model_ok else "degraded"
    return HealthResponse(
        status=overall,
        db="ok" if db_ok else "fail",
        redis="ok" if redis_ok else "fail",
        model="ok" if model_ok else "fail",
    )
