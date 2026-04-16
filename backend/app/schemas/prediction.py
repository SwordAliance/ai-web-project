from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict


class PredictRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Сделай краткое описание архитектуры проекта",
                "creativity": 0.4,
            }
        }
    )

    prompt: str = Field(..., min_length=1, max_length=500, description="Текст запроса")
    creativity: float = Field(..., ge=0.0, le=1.0, description="Коэффициент креативности от 0 до 1")


class PredictResponse(BaseModel):
    task_id: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    prompt: str | None = None
    creativity: float | None = None
    result: str | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    db: str
    redis: str
    model: str


class HistoryItem(BaseModel):
    task_id: str
    prompt: str
    creativity: float
    status: str
    result: str | None = None
    error: str | None = None


class HistoryResponse(BaseModel):
    items: list[HistoryItem]
