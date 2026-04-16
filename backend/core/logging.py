from __future__ import annotations

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    # Логирование всех этапов работы приложения
    root = logging.getLogger()
    if root.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
    root.setLevel(level.upper())
