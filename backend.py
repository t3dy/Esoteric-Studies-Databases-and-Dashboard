import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Ensure backend package is resolvable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app_v2.main import app as app_v2
from backend.app_v3.main import app as app_v3

# Gateway App
app = FastAPI(title="Esoteric Knowledge Engine (Gateway)", version="3.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount V2 (Legacy + Root for backward compat)
app.mount("/api/v2", app_v2)
# We also mount V2 at /api because the Frontend expects it there by default
app.mount("/api", app_v2) 

# Mount V3 (Hermetic)
app.mount("/api/v3", app_v3)

# Mount Static Files (Dashboard)
if os.path.exists("dashboard/dist"):
    app.mount("/", StaticFiles(directory="dashboard/dist", html=True), name="static")

if __name__ == "__main__":
    print("🚀 Starting Gateway: V2 (Legacy) + V3 (Hermetic)")
    print("   - V2 API: http://localhost:8000/api")
    print("   - V3 API: http://localhost:8000/api/v3")
    uvicorn.run(app, host="0.0.0.0", port=8000)
