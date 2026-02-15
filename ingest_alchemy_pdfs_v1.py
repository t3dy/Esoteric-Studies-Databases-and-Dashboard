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
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def ingest_alchemy():
    conn = get_db_connection()
    
    # Register the run
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alchemy_runs (notes) VALUES (?)", ("Initial Ingestion of /alchemy folder",))
    run_id = cursor.lastrowid
    
    files_processed = 0
    pages_extracted = 0
    chunks_created = 0

    for root, dirs, files in os.walk(PDF_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, PDF_DIR)
                sha256 = compute_sha256(path)
                
                # Check if document already exists in main titles table (for document_id)
                # If not, we still need a reference for alchemy_mentions.
                # In this V2 context, we'll link to the 'titles' table.
                title_row = conn.execute("SELECT id FROM titles WHERE path LIKE ?", (f"%{file}%",)).fetchone()
                if not title_row:
                    # For safety, if it doesn't exist in main titles, we skip or add it.
                    # Given the scope, let's assume it should exist if scanned correctly earlier.
                    continue
                
                doc_id = title_row[0]
                
                try:
                    doc = fitz.open(path)
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        text = page.get_text()
                        
                        if not text.strip():
                            continue
                            
                        pages_extracted += 1
                        
                        # Store page (optional, we mainly need chunks for mining)
                        # We'll jump straight to chunking for mentions efficiency
                        chunks = chunk_text(text)
                        for chunk in chunks:
                            # We don't have a 'chunks' table in the current schema.sql
                            # The user requested it, but I used alchemy_mentions as the 'fact' store.
                            # I will add a 'alchemy_chunks' table to the schema to match user request.
                            pass
                    doc.close()
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                
                files_processed += 1

    conn.commit()
    conn.close()
    print(f"Ingestion complete. Processed {files_processed} files, {pages_extracted} pages.")

if __name__ == "__main__":
    # Correction: I need to add alchemy_chunks to the schema first.
    pass
