from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://ai_user:ai_pass@postgres:5432/ai_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    model_max_input_chars: int = int(os.getenv("MODEL_MAX_INPUT_CHARS", "500"))
    model_max_output_chars: int = int(os.getenv("MODEL_MAX_OUTPUT_CHARS", "1200"))


settings = Settings()
