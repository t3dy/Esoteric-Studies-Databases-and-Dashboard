import sqlite3
import os
import fitz  # PyMuPDF
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

# Paths to the various esoteric folders
CORPUS_PATHS = {
    "hermetic": "e:\\pdf\\hermetic",
    "gnostic": "e:\\pdf\\ancient magic gnostic pgm etc",
    "rosicrucian": "e:\\pdf\\Rosicrucian",
    "crowley": "e:\\pdf\\crowley",
    "esoteric_studies": "e:\\pdf\\western esotericism religious studies"
}

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

def ingest_historiography():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Register Run
    cursor.execute("INSERT INTO alchemy_runs (run_type, notes) VALUES (?, ?)", 
                   ("ingest_historiography", "Cross-corpus ingestion of Hermetic, Gnostic, Rosicrucian, and Crowley materials"))
    run_id = cursor.lastrowid
    
    for domain, folder_path in CORPUS_PATHS.items():
        if not os.path.exists(folder_path):
            print(f"Skipping {domain} (path not found: {folder_path})")
            continue
            
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        print(f"Found {len(files)} files in {domain} corpus.")
        
        for filename in files:
            path = os.path.join(folder_path, filename)
            try:
                file_hash = compute_file_hash(path)
                
                # Check for existing document
                # Using the NEW file_hash column from V3
                exists = cursor.execute("SELECT id FROM alchemy_documents WHERE file_hash = ?", (file_hash,)).fetchone()
                if exists:
                    print(f"  - Skipping {filename} (already exists)")
                    continue
                
                print(f"  - Ingesting {filename}...")
                doc = fitz.open(path)
                cursor.execute("""
                    INSERT INTO alchemy_documents (title, path, file_hash, domain, run_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (filename, path, file_hash, domain, run_id))
                doc_id = cursor.lastrowid
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    
                    cursor.execute("INSERT INTO alchemy_pages (document_id, page_number, raw_text) VALUES (?, ?, ?)",
                                   (doc_id, page_num + 1, text))
                    page_db_id = cursor.lastrowid
                    
                    chunk_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
                    cursor.execute("""
                        INSERT INTO alchemy_chunks (page_id, document_id, text_clean, chunk_hash)
                        VALUES (?, ?, ?, ?)
                    """, (page_db_id, doc_id, text.replace('\x00', ''), chunk_hash))
                
                doc.close()
            except Exception as e:
                print(f"  - Error in {filename}: {e}")
            
            conn.commit() # Commit per document for safety
            
    conn.close()
    print("Historiographical ingestion complete.")

if __name__ == "__main__":
    ingest_historiography()
