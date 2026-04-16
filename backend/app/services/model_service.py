from __future__ import annotations

import logging
import time

from app.core.config import settings

logger = logging.getLogger(__name__)


class ModelService:
    # ML-логика изолирована в отдельном классе
    def __init__(self) -> None:
        self.max_input_chars = settings.model_max_input_chars
        self.max_output_chars = settings.model_max_output_chars
        self._ready = True

    def is_ready(self) -> bool:
        return self._ready

    def generate(self, prompt: str, creativity: float) -> tuple[str, list[dict[str, float | str]]]:
        start = time.perf_counter()

        cleaned = prompt.strip()[: self.max_input_chars]
        base = f"Ответ на запрос: {cleaned}"
        suffix = f" | creativity={creativity:.2f}"
        text = (base + suffix)[: self.max_output_chars]

        alternatives = [
            {"intent": "summary", "score": 0.82},
            {"intent": "steps", "score": 0.66},
            {"intent": "code", "score": 0.73},
        ]

        time.sleep(1.2)  # имитация работы модели

        elapsed = time.perf_counter() - start
        logger.info("model_generate finished in %.3fs", elapsed)
        return text, alternatives


_model_service: ModelService | None = None


def get_model_service() -> ModelService:
    global _model_service
    if _model_service is None:
        _model_service = ModelService()
    return _model_service
