import sqlite3
import json
import os
import re

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def detect_experiment(text):
    # Rule-based detection: high density of imperatives
    imperatives = [r"\btake\b", r"\badd\b", r"\bheat\b", r"\bdistill\b", r"\bgrind\b", r"\bmix\b", r"\bplace\b", r"\bput\b"]
    matches = []
    for imp in imperatives:
        matches.extend(re.findall(imp, text, re.IGNORECASE))
    
    # If we have at least 3 imperatives in a chunk, it's likely a procedure
    return len(matches) >= 3

def extract_experiments():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Register the run
    cursor.execute("INSERT INTO alchemy_runs (notes) VALUES (?)", ("Experiment procedural extraction run",))
    run_id = cursor.lastrowid
    
    experiments_found = 0

    # Iterate chunks
    chunks = conn.execute("SELECT id, text_clean FROM alchemy_chunks").fetchall()
    
    for chunk in chunks:
        text = chunk['text_clean']
        if detect_experiment(text):
            # Try to identify a title (first sentence or first few words)
            title = " ".join(text.split()[:10]) + "..."
            
            # Simple step extraction (splitting by periods/punctuation)
            steps = [s.strip() for s in re.split(r'[.!?]\s+', text) if len(s.strip()) > 10]
            
            # We don't have a specific alchemy_experiments table in the final user-spec schema
            # Wait, the user asked for: documents, pages, chunks, entities, entity_aliases, mentions, relationships, runs.
            # Experiments are procedural text. I should store them as entities with category 'I' (Experiments)
            # and potentially detailed metadata in metadata_json.
            
            entity_id = str(uuid_v4()) # I'll just use the entity table for consistency
            
            # Re-reviewing user prompt: "extract_experiments.py: detect procedural text and output structured “experiment” entities and step lists"
            # I will store the steps in metadata_json of the 'Experiments' entity.
            
            cursor.execute("""
                INSERT INTO alchemy_entities (id, category, canonical_name, normalized_name, metadata_json, run_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(os.urandom(16).hex()), # UUID fallback
                'I', # Category I: Experiments
                title,
                title.lower()[:50],
                json.dumps({"steps": steps, "type": "procedural"}),
                run_id
            ))
            
            experiments_found += 1

    conn.commit()
    conn.close()
    print(f"Extraction complete. Found {experiments_found} experiments.")

if __name__ == "__main__":
    extract_experiments()
