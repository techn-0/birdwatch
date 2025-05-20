# app/routes/ws.py
from fastapi import APIRouter, WebSocket
from ..ws import manager

router = APIRouter()

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()   # 클라이언트 ping 용
    except:
        manager.disconnect(ws)
