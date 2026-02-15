import os
import fitz  # PyMuPDF
import sqlite3
import hashlib
import uuid
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")
PDF_DIR = r"e:\pdf\alchemy"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def chunk_text(text, chunk_size=1000, overlap=150):
    words = text.split()
    chunks = []
    # Simplified character-based indexing for char_start/end
    # Note: In a production setting, you'd use a more precise offset tracker.
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        chunk = " ".join(chunk_words)
        if chunk:
            chunks.append(chunk)
    return chunks

def ingest_alchemy():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Register the run
    cursor.execute("INSERT INTO alchemy_runs (notes) VALUES (?)", ("Alchemy Corpus Ingestion and Chunking",))
    run_id = cursor.lastrowid
    
    files_processed = 0
    pages_stored = 0
    chunks_created = 0

    for root, dirs, files in os.walk(PDF_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, PDF_DIR)
                sha256 = compute_sha256(path)
                
                # Check if document already exists
                existing_doc = cursor.execute("SELECT id, sha256 FROM alchemy_documents WHERE path = ?", (path,)).fetchone()
                if existing_doc:
                    if existing_doc['sha256'] == sha256:
                        print(f"Skipping {file} (Unchanged)")
                        continue
                    else:
                        # Clear old data for this doc if changed
                        cursor.execute("DELETE FROM alchemy_chunks WHERE document_id = ?", (existing_doc['id'],))
                        cursor.execute("DELETE FROM alchemy_pages WHERE document_id = ?", (existing_doc['id'],))
                        cursor.execute("UPDATE alchemy_documents SET sha256 = ?, added_at = ? WHERE id = ?", (sha256, datetime.now(), existing_doc['id']))
                        doc_id = existing_doc['id']
                else:
                    cursor.execute("INSERT INTO alchemy_documents (path, title, folder, sha256) VALUES (?, ?, ?, ?)", (path, file, os.path.basename(root), sha256))
                    doc_id = cursor.lastrowid
                
                try:
                    doc = fitz.open(path)
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        text_raw = page.get_text()
                        
                        if not text_raw.strip():
                            continue
                            
                        cursor.execute("INSERT INTO alchemy_pages (document_id, page_no, text_raw) VALUES (?, ?, ?)", (doc_id, page_num + 1, text_raw))
                        
                        # Chunking
                        chunks = chunk_text(text_raw)
                        for chunk in chunks:
                            chunk_sha = hashlib.sha256(chunk.encode()).hexdigest()
                            # text_clean normalization (simplified)
                            text_clean = " ".join(chunk.split())
                            
                            cursor.execute("""
                                INSERT INTO alchemy_chunks (document_id, page_start, page_end, text_clean, sha256)
                                VALUES (?, ?, ?, ?, ?)
                            """, (doc_id, page_num + 1, page_num + 1, text_clean, chunk_sha))
                            chunks_created += 1
                        
                        pages_stored += 1
                    doc.close()
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                
                files_processed += 1
                if files_processed % 10 == 0:
                    conn.commit()
                    print(f"Progress: {files_processed} files...")

    conn.commit()
    conn.close()
    print(f"Ingestion complete. Files: {files_processed}, Pages: {pages_stored}, Chunks: {chunks_created}")

if __name__ == "__main__":
    ingest_alchemy()
