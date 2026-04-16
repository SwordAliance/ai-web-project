from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self._connections: DefaultDict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, task_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[task_id].add(websocket)

    def disconnect(self, task_id: str, websocket: WebSocket) -> None:
        if task_id in self._connections:
            self._connections[task_id].discard(websocket)
            if not self._connections[task_id]:
                self._connections.pop(task_id, None)

    async def broadcast(self, task_id: str, payload: dict) -> None:
        sockets = list(self._connections.get(task_id, set()))
        for websocket in sockets:
            try:
                await websocket.send_json(payload)
            except Exception:
                self.disconnect(task_id, websocket)


manager = WebSocketManager()
