from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.ws_manager import manager

router = APIRouter(tags=["websocket"])


@router.websocket("/api/ws/{task_id}")
async def websocket_task(websocket: WebSocket, task_id: str) -> None:
    await manager.connect(task_id, websocket)
    try:
        while True:
            # Поддерживаем живое соединение; клиент может отправлять ping
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(task_id, websocket)
