import sqlite3
import uuid
import json
import os
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V2_DB = "library.db"
V3_DB = "library_v3.db"

RUN_ID = str(uuid.uuid4())
RUN_TS = datetime.now().isoformat()

def get_v2_conn():
    if not os.path.exists(V2_DB):
        raise FileNotFoundError(f"V2 DB not found: {V2_DB}")
    return sqlite3.connect(V2_DB)

def get_v3_conn():
    conn = sqlite3.connect(V3_DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def log(msg):
    print(f"[Import] {msg}")

def run_import():
    log(f"Starting Import Run: {RUN_ID}")
    
    v2 = get_v2_conn()
    v3 = get_v3_conn()
    
    try:
        # 1. Register Run
        v3.execute("""
            INSERT INTO runs (id, run_type, params_json, status, notes) 
            VALUES (?, ?, ?, ?, ?)
        """, (RUN_ID, "import", json.dumps({"source": "v2_library.db"}), "running", "Lift and Shift Import"))
        
        # 2. Import File Manifest (from V2 titles or documents)
        # V2 Schema varies, we check 'documents' or 'titles'
        cursor = v2.cursor()
        tables = [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        
        files_count = 0
        if 'documents' in tables:
             # Assuming V2 documents: id, path, title...
             # We might need to hash them now if V2 didn't have hashes.
             # For speed, we might assume path identity or generate hash if file exists.
             rows = v2.execute("SELECT path, title FROM documents").fetchall()
             for path, title in rows:
                 file_hash = str(uuid.uuid5(uuid.NAMESPACE_URL, path)) # Temporary stable hash based on path
                 v3.execute("""
                    INSERT OR IGNORE INTO file_manifest (file_hash, current_path, status)
                    VALUES (?, ?, 'active')
                 """, (file_hash, path))
                 
                 doc_id = str(uuid.uuid4())
                 v3.execute("""
                    INSERT INTO documents (id, file_hash, title, run_id)
                    VALUES (?, ?, ?, ?)
                 """, (doc_id, file_hash, title, RUN_ID))
                 files_count += 1
        
        elif 'titles' in tables:
            # V1/V2 legacy
            rows = v2.execute("SELECT path, title FROM titles").fetchall()
            for path, title in rows:
                 file_hash = str(uuid.uuid5(uuid.NAMESPACE_URL, path))
                 v3.execute("""
                    INSERT OR IGNORE INTO file_manifest (file_hash, current_path, status)
                    VALUES (?, ?, 'active')
                 """, (file_hash, path))
                 
                 doc_id = str(uuid.uuid4())
                 v3.execute("""
                    INSERT INTO documents (id, file_hash, title, run_id)
                    VALUES (?, ?, ?, ?)
                 """, (doc_id, file_hash, title, RUN_ID))
                 files_count += 1
                 
        log(f"Imported {files_count} documents.")

        # 3. Import Entities (if v2 has them)
        # Normalizing to V3 strict categories
        entities_count = 0
        if 'entities' in tables:
            rows = v2.execute("SELECT canonical_name, category FROM entities").fetchall()
            for name, cat in rows:
                ent_id = str(uuid.uuid4())
                norm = name.lower().strip()
                # Map categories
                v3_cat = "CONCEPT"
                if cat.upper() in ['ALCHEMIST', 'AUTHOR']: v3_cat = 'ALCHEMIST'
                if cat.upper() in ['PROCESS', 'OPERATION']: v3_cat = 'PROCESS'
                if cat.upper() in ['MATERIAL', 'SUBSTANCE']: v3_cat = 'MATERIAL'
                
                v3.execute("""
                    INSERT INTO entities (id, canonical_name, normalized_name, category, run_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (ent_id, name, norm, v3_cat, RUN_ID))
                entities_count += 1
        
        log(f"Imported {entities_count} entities.")

        # 4. Commit Run
        v3.execute("UPDATE runs SET status='success', finished_at=CURRENT_TIMESTAMP WHERE id=?", (RUN_ID,))
        v3.commit()
        log("Import Complete SUCCESS")

    except Exception as e:
        v3.execute("UPDATE runs SET status='failed', notes=? WHERE id=?", (str(e), RUN_ID))
        v3.commit()
        log(f"Import FAILED: {e}")
        raise
    finally:
        v2.close()
        v3.close()

if __name__ == "__main__":
    run_import()
