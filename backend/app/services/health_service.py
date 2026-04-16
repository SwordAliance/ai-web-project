from __future__ import annotations

from sqlalchemy import text

from app.db.session import SessionLocal
from app.services.model_service import get_model_service
from redis import Redis
from app.core.config import settings


def check_database() -> bool:
    with SessionLocal() as session:
        session.execute(text("SELECT 1"))
    return True


def check_redis() -> bool:
    client = Redis.from_url(settings.redis_url)
    try:
        return bool(client.ping())
    finally:
        client.close()


def check_model() -> bool:
    return get_model_service().is_ready()
