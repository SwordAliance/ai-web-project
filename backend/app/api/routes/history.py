from __future__ import annotations

from fastapi import APIRouter

from app.db.session import SessionLocal
from app.db.repositories import list_recent_requests
from app.schemas.prediction import HistoryItem, HistoryResponse

router = APIRouter(tags=["history"])


@router.get("/history", response_model=HistoryResponse)
def history(limit: int = 10) -> HistoryResponse:
    with SessionLocal() as db:
        items = list_recent_requests(db, limit=limit)

    return HistoryResponse(
        items=[
            HistoryItem(
                task_id=item.task_id,
                prompt=item.prompt,
                creativity=item.creativity,
                status=item.status,
                result=item.result,
                error=item.error,
            )
            for item in items
        ]
    )
