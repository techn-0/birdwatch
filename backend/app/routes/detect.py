from fastapi import APIRouter, WebSocket
from ..db import db
from ..models import Detection
from datetime import datetime

router = APIRouter()
sockets: list[WebSocket] = []     # 간단 브로드캐스트용

@router.post("/detect/result")
async def ingest(det: Detection):
    col = db[f"detections_{det.captured_at:%Y%m}"]
    await col.insert_one(det.dict())
    # WebSocket 브로드캐스트
    for ws in sockets:
        await ws.send_json(det.dict())
    return {"ok": True}

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    sockets.append(ws)
    try:
        while True:
            await ws.receive_text()   # ping용
    except:
        sockets.remove(ws)
