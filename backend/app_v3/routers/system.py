from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
import sqlite3

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/health")
def health_check():
    return {"status": "online", "mode": "hermetic_v3", "version": "3.0.0"}

@router.get("/stats")
def v3_stats(db: Session = Depends(get_db)):
    # Raw SQL for speed on counts
    try:
        docs = db.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        entities = db.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        rels = db.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
        runs = db.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        return {
            "documents": docs,
            "entities": entities,
            "relationships": rels,
            "runs": runs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/runs")
def list_runs(limit: int = 10, db: Session = Depends(get_db)):
    res = db.execute(f"SELECT * FROM runs ORDER BY started_at DESC LIMIT {limit}").fetchall()
    return [dict(r) for r in res]
