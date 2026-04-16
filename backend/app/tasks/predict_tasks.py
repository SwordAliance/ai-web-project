from __future__ import annotations

import json
import logging

import redis
from celery import Task

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.repositories import create_request_log, update_request_log
from app.services.model_service import get_model_service
from app.tasks.celery_app import celery

logger = logging.getLogger(__name__)


def _publish(channel: str, payload: dict) -> None:
    client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    try:
        client.publish(channel, json.dumps(payload, ensure_ascii=False))
    finally:
        client.close()


@celery.task(bind=True, name="generate_prediction")
def generate_prediction(self: Task, prompt: str, creativity: float) -> dict:
    task_id = self.request.id

    with SessionLocal() as db:
        create_request_log(db, task_id, prompt, creativity)
        update_request_log(db, task_id, status="started")

    _publish(f"task:{task_id}", {"task_id": task_id, "status": "started"})

    try:
        model = get_model_service()
        result, alternatives = model.generate(prompt, creativity)

        with SessionLocal() as db:
            update_request_log(db, task_id, status="success", result=result, error=None)

        payload = {
            "task_id": task_id,
            "status": "success",
            "result": result,
            "alternatives": alternatives,
        }
        _publish(f"task:{task_id}", payload)
        return payload
    except Exception as exc:
        error_text = str(exc)
        logger.exception("Task failed")
        with SessionLocal() as db:
            update_request_log(db, task_id, status="failed", result=None, error=error_text)

        payload = {
            "task_id": task_id,
            "status": "failed",
            "error": error_text,
        }
        _publish(f"task:{task_id}", payload)
        raise
