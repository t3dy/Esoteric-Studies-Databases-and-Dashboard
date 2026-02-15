import os
import fitz  # PyMuPDF
import hashlib
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")
PDF_DIR = r"e:\pdf\alchemy\poetry lit"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def get_file_hash(path):
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def ingest_poetry_pdfs():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if not os.path.exists(PDF_DIR):
        print(f"Poetry folder not found: {PDF_DIR}")
        return

    for root, dirs, files in os.walk(PDF_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                sha256 = get_file_hash(full_path)
                
                # Check if already ingested
                cursor.execute("SELECT id, sha256 FROM alchemy_documents WHERE path = ?", (full_path,))
                existing = cursor.fetchone()
                
                if existing:
                    if existing[1] == sha256:
                        print(f"Skipping {file} (Unchanged)")
                        continue
                    else:
                        print(f"Updating {file} (Changed)")
                        # Delete old pages/chunks if file changed
                        cursor.execute("DELETE FROM alchemy_pages WHERE document_id = ?", (existing[0],))
                        cursor.execute("DELETE FROM alchemy_chunks WHERE document_id = ?", (existing[0],))
                        cursor.execute("UPDATE alchemy_documents SET sha256 = ? WHERE id = ?", (sha256, existing[0]))
                        doc_id = existing[0]
                else:
                    cursor.execute("INSERT INTO alchemy_documents (path, title, folder, sha256) VALUES (?, ?, ?, ?)",
                                 (full_path, file, "poetry lit", sha256))
                    doc_id = cursor.lastrowid

                # Extract Pages
                print(f"Extracting {file}...")
                try:
                    doc = fitz.open(full_path)
                    for page_no, page in enumerate(doc):
                        text = page.get_text()
                        cursor.execute("INSERT INTO alchemy_pages (document_id, page_no, text_raw) VALUES (?, ?, ?)",
                                     (doc_id, page_no + 1, text))
                except Exception as e:
                    print(f"Error reading {file}: {e}")
                
                conn.commit()

    conn.close()
    print("Poetry ingestion complete.")

if __name__ == "__main__":
    ingest_poetry_pdfs()
