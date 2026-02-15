import sqlite3
import json
import os
import re

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def detect_reconstruction(text):
    # Pattern for modern researchers and reconstruction keywords
    modern_scholars = ["Principe", "Newman", "Kauffman", "Principe and Newman"]
    keywords = ["reconstructed", "replicated", "reproduced", "attempted", "reconstruction"]
    
    scholar_found = any(s.lower() in text.lower() for s in modern_scholars)
    keyword_found = any(k.lower() in text.lower() for k in keywords)
    
    return scholar_found and keyword_found

def extract_reconstructions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Register the run
    cursor.execute("INSERT INTO alchemy_runs (notes) VALUES (?)", ("Modern alchemical reconstruction detection run",))
    run_id = cursor.lastrowid
    
    reconstructions_found = 0

    # Iterate chunks
    chunks = conn.execute("SELECT id, document_id, text_clean FROM alchemy_chunks").fetchall()
    
    for chunk in chunks:
        text = chunk['text_clean']
        if detect_reconstruction(text):
            # Extract basic context
            title = "Reconstruction: " + " ".join(text.split()[:8]) + "..."
            
            # Store in 'Reconstructions' category (J)
            cursor.execute("""
                INSERT INTO alchemy_entities (id, category, canonical_name, normalized_name, metadata_json, run_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(os.urandom(16).hex()),
                'J', # Category J: Reconstructions
                title,
                title.lower()[:50],
                json.dumps({"description": text[:500], "type": "modern_reconstruction"}),
                run_id
            ))
            
            reconstructions_found += 1

    conn.commit()
    conn.close()
    print(f"Extraction complete. Found {reconstructions_found} reconstructions.")

if __name__ == "__main__":
    extract_reconstructions()
