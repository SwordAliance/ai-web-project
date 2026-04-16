from __future__ import annotations

import asyncio
import json
import logging

import redis.asyncio as redis

from app.core.config import settings
from app.services.ws_manager import manager

logger = logging.getLogger(__name__)


async def redis_listener() -> None:
    # Listener работает в фоне и ретранслирует сообщения из Redis в WebSocket
    client = redis.from_url(settings.redis_url, decode_responses=True)
    pubsub = client.pubsub()
    await pubsub.psubscribe("task:*")

    try:
        async for message in pubsub.listen():
            if message is None:
                await asyncio.sleep(0.1)
                continue

            if message.get("type") not in {"pmessage", "message"}:
                continue

            raw_data = message.get("data")
            if not raw_data or not isinstance(raw_data, str):
                continue

            try:
                payload = json.loads(raw_data)
            except json.JSONDecodeError:
                logger.warning("Invalid JSON in Redis message")
                continue

            task_id = payload.get("task_id")
            if task_id:
                await manager.broadcast(task_id, payload)
    except asyncio.CancelledError:
        raise
    except Exception:
        logger.exception("Redis listener stopped unexpectedly")
        raise
    finally:
        await pubsub.aclose()
        await client.aclose()
