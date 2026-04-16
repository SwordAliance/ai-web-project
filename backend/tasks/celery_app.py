from __future__ import annotations

import os

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery(
    "ai_web_service",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.predict_tasks"],
)

celery.conf.update(
    task_track_started=True,
    result_expires=3600,
    broker_connection_retry_on_startup=True,
)
