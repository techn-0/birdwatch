from fastapi import FastAPI
from app.routes import detect, cctv

app = FastAPI()
app.include_router(detect.router)
app.include_router(cctv.router)

@app.get("/ping") # 헬스체크
async def ping():
    return {"ok": True}
