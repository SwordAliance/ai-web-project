from __future__ import annotations

from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.db.models import RequestLog


def create_request_log(db: Session, task_id: str, prompt: str, creativity: float) -> RequestLog:
    item = RequestLog(
        task_id=task_id,
        prompt=prompt,
        creativity=creativity,
        status="queued",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_request_log(db: Session, task_id: str, *, status: str, result: str | None = None, error: str | None = None) -> RequestLog | None:
    item = db.scalar(select(RequestLog).where(RequestLog.task_id == task_id))
    if item is None:
        return None
    item.status = status
    item.result = result
    item.error = error
    db.commit()
    db.refresh(item)
    return item


def get_request_log(db: Session, task_id: str) -> RequestLog | None:
    return db.scalar(select(RequestLog).where(RequestLog.task_id == task_id))


def list_recent_requests(db: Session, limit: int = 10) -> list[RequestLog]:
    stmt = select(RequestLog).order_by(desc(RequestLog.created_at)).limit(limit)
    return list(db.scalars(stmt).all())
