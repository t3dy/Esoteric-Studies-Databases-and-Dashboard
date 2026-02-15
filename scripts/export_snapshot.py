import sqlite3
import json
import os
import shutil
from datetime import datetime

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "library_v3.db")
EXPORT_DIR = os.path.join(BASE_DIR, "dashboard", "public", "data", "latest")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def safe_json(rows):
    return [dict(row) for row in rows]

def export_snapshot():
    print(f"Exporting Snapshot from {DB_PATH} to {EXPORT_DIR}...")
    
    if not os.path.exists(DB_PATH):
        print("Error: V3 Database not found. Run migrations/import first.")
        return

    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    conn = get_db()
    
    try:
        # 1. Manifest
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "db_version": "3.0.0",
            "note": "Static Export for GitHub Pages"
        }
        with open(os.path.join(EXPORT_DIR, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)
            
        # 2. Stats
        docs_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        ent_count = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        rel_count = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
        stats = {
            "documents": docs_count,
            "entities": ent_count,
            "relationships": rel_count,
            "storage_mode": "Static JSON"
        }
        with open(os.path.join(EXPORT_DIR, "stats.json"), "w") as f:
            json.dump(stats, f, indent=2)
            
        # 3. Entities (Capped at 5000)
        entities = conn.execute("""
            SELECT id, canonical_name, category, domain, confidence, historiography_tags 
            FROM entities 
            ORDER BY confidence DESC 
            LIMIT 5000
        """).fetchall()
        with open(os.path.join(EXPORT_DIR, "entities.json"), "w") as f:
            json.dump(safe_json(entities), f)

        # 4. Relationships (Capped at 10000)
        rels = conn.execute("""
            SELECT r.subject_entity_id, r.predicate, r.object_entity_id, r.confidence,
                   e1.canonical_name as subject_name, e2.canonical_name as object_name
            FROM relationships r
            JOIN entities e1 ON r.subject_entity_id = e1.id
            JOIN entities e2 ON r.object_entity_id = e2.id
            LIMIT 10000
        """).fetchall()
        with open(os.path.join(EXPORT_DIR, "relationships.json"), "w") as f:
            json.dump(safe_json(rels), f)

        # 5. Documents (Full list usually okay if <10k)
        docs = conn.execute("SELECT id, title, type, domain, added_at FROM documents").fetchall() # fixed doc_type to type or check schema
        # Schema says doc_type, let's check schema/migration 001. 
        # Migration 001 says 'doc_type'.
        # I'll stick to * for safety or check columns.
        docs = conn.execute("SELECT id, title, doc_type, domain, added_at FROM documents").fetchall()
        with open(os.path.join(EXPORT_DIR, "docs.json"), "w") as f:
            json.dump(safe_json(docs), f)
            
        print("Success: Snapshot Exported.")
        
    except Exception as e:
        print(f"Export Failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_snapshot()
