from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import sqlite3
import uvicorn
from contextlib import asynccontextmanager

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "library_v3.db") # NEW V3 DB
V2_DB_PATH = os.path.join(BASE_DIR, "library.db") # LEGACY DB

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Check Schema Version
    check_schema()
    yield
    # Shutdown

app = FastAPI(title="Esoteric Knowledge Engine V3", lifespan=lifespan)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def check_schema():
    if not os.path.exists(DB_PATH):
        print("V3 DB not found. Please run migrations.")
        return
    try:
        conn = get_db()
        ver = conn.execute("SELECT MAX(version_number) FROM schema_version").fetchone()[0]
        print(f"V3 Database Version: {ver}")
        conn.close()
    except Exception as e:
        print(f"Schema Check Failed: {e}")

@app.get("/api/v3/health")
def health_check():
    return {"status": "online", "version": "3.0.0", "mode": "hermetic"}

@app.get("/api/v3/stats")
def v3_stats():
    conn = get_db()
    try:
        docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        entities = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        rels = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
        return {"documents": docs, "entities": entities, "relationships": rels}
    finally:
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
