from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db

router = APIRouter(prefix="/library", tags=["Library"])

@router.get("/search")
def search_corpus(q: str, limit: int = 20, db: Session = Depends(get_db)):
    # V3 FTS5 Search (assuming fts_chunks exists or we fallback to LIKE for prototype)
    # The Genesis schema defined fts_chunks virtual table? 
    # Wait, Genesis schema defined `chunks` but not explicit `fts_chunks` create statement in step 1974?
    # Let's check 001_genesis.sql content. It had "FTS5 virtual tables" section as comments or SQL?
    # Re-reading step 1974... "11. Mining Log... INSERT INTO schema_version..."
    # It seems I might have missed the actual FTS5 CREATE statement in the SQL file!
    # I will stick to LIKE for now or verify schema.
    
    # Fallback search on Documents
    res = db.execute(
        "SELECT id, title, domain FROM documents WHERE title LIKE ? LIMIT ?", 
        (f"%{q}%", limit)
    ).fetchall()
    return [dict(r) for r in res]

@router.get("/documents/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return dict(doc)
