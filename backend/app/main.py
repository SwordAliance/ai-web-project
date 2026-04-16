from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes.health import router as health_router
from app.api.routes.history import router as history_router
from app.api.routes.predict import router as predict_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.ws import router as ws_router
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging
from app.services.ws_listener import redis_listener

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lifespan: инициализация фоновых задач и инфраструктуры
    configure_logging()
    listener_task = asyncio.create_task(redis_listener())
    try:
        yield
    finally:
        listener_task.cancel()
        try:
            await listener_task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="AI Web Service", version="1.0.0", lifespan=lifespan)
register_exception_handlers(app)

app.include_router(health_router, prefix="/api")
app.include_router(predict_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(ws_router)

# Метрики Prometheus
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
