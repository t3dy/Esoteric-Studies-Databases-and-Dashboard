import sqlite3
import os
import fitz  # PyMuPDF
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")
HERMETIC_ROOT = "e:\\pdf\\hermetic"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def compute_file_hash(path):
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def ingest_hermetic():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Register Run
    cursor.execute("INSERT INTO alchemy_runs (run_type, notes) VALUES (?, ?)", ("ingest_hermetic", "Ingestion of Hermetic and Late Antique corpus"))
    run_id = cursor.lastrowid
    
    files = [f for f in os.listdir(HERMETIC_ROOT) if f.lower().endswith('.pdf')]
    print(f"Found {len(files)} Hermetic files.")
    
    for filename in files:
        path = os.path.join(HERMETIC_ROOT, filename)
        file_hash = compute_file_hash(path)
        
        # Check if already exists
        exists = cursor.execute("SELECT id FROM alchemy_documents WHERE file_hash = ?", (file_hash,)).fetchone()
        if exists:
            print(f"Skipping {filename} (already ingested).")
            continue
            
        print(f"Ingesting {filename}...")
        try:
            doc = fitz.open(path)
            cursor.execute("""
                INSERT INTO alchemy_documents (title, file_path, file_hash, domain, run_id)
                VALUES (?, ?, ?, ?, ?)
            """, (filename, path, file_hash, "hermetic", run_id))
            doc_id = cursor.lastrowid
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                cursor.execute("""
                    INSERT INTO alchemy_pages (document_id, page_number, raw_text)
                    VALUES (?, ?, ?)
                """, (doc_id, page_num + 1, text))
                page_db_id = cursor.lastrowid
                
                # Create a single chunk per page for now
                chunk_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
                cursor.execute("""
                    INSERT INTO alchemy_chunks (page_id, document_id, text_clean, chunk_hash)
                    VALUES (?, ?, ?, ?)
                """, (page_db_id, doc_id, text, chunk_hash))
            
            doc.close()
        except Exception as e:
            print(f"Error ingesting {filename}: {e}")
            
    conn.commit()
    conn.close()
    print("Hermetic ingestion complete.")

if __name__ == "__main__":
    ingest_hermetic()
