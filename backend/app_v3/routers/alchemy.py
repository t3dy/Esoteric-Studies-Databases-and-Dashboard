from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db

router = APIRouter(prefix="/alchemy", tags=["Alchemy"])

@router.get("/entities")
def list_entities(category: str = None, limit: int = 50, db: Session = Depends(get_db)):
    sql = "SELECT * FROM entities"
    params = []
    if category:
        sql += " WHERE category = ?"
        params.append(category)
    sql += f" LIMIT {limit}"
    
    res = db.execute(sql, tuple(params)).fetchall()
    return [dict(r) for r in res]

@router.get("/graph/{entity_id}")
def get_entity_graph(entity_id: str, db: Session = Depends(get_db)):
    # Center node
    entity = db.execute("SELECT * FROM entities WHERE id = ?", (entity_id,)).fetchone()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    # Relationships
    rels = db.execute("""
        SELECT r.*, e.canonical_name as target_name, e.category as target_category
        FROM relationships r
        JOIN entities e ON r.object_entity_id = e.id
        WHERE r.subject_entity_id = ?
    """, (entity_id,)).fetchall()
    
    return {
        "entity": dict(entity),
        "relationships": [dict(r) for r in rels]
    }
