from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import sqlite3
import uvicorn
from contextlib import asynccontextmanager

from .routers import system, library, alchemy
from .core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup check
    if not os.path.exists(settings.DB_URL.replace("sqlite:///", "")):
        print(f"WARNING: V3 DB not found at {settings.DB_URL}")
    yield

app = FastAPI(title="Esoteric Knowledge Engine V3", lifespan=lifespan)

# Include Routers
app.include_router(system.router)
app.include_router(library.router)
app.include_router(alchemy.router)

# Observability: Mining Log WebSocket
@app.websocket("/ws/mining")
async def websocket_mining_log(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # simple echo/heartbeat for now, real implementation would hook into Event Bus
            data = await websocket.receive_text()
            await websocket.send_text(f"Run Log: {data}")
    except Exception:
        pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
