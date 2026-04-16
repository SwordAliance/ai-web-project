from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db.session import SessionLocal
from app.db.repositories import get_request_log
from app.schemas.prediction import TaskStatusResponse

router = APIRouter(tags=["tasks"])


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
def get_task_status(task_id: str) -> TaskStatusResponse:
    with SessionLocal() as db:
        item = get_request_log(db, task_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        return TaskStatusResponse(
            task_id=item.task_id,
            status=item.status,
            prompt=item.prompt,
            creativity=item.creativity,
            result=item.result,
            error=item.error,
        )
