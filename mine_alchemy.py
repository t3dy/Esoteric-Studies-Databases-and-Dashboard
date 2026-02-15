import sqlite3
import json
import os
import uuid
import re
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")
LEXICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alchemy_lexicon.json")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_lexicon():
    with open(LEXICON_PATH, "r") as f:
        return json.load(f)

def normalize(text):
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

def mine_alchemy():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Register the run
    cursor.execute("INSERT INTO alchemy_runs (notes) VALUES (?)", ("Lexicon-based entity mining run",))
    run_id = cursor.lastrowid
    
    lexicon = load_lexicon()
    entities_mined = 0
    mentions_created = 0

    # We iterate chunks
    chunks = conn.execute("SELECT id, document_id, text_clean FROM alchemy_chunks").fetchall()
    
    # Pre-cache existing entities to avoid duplicates
    existing_entities = {normalize(row['canonical_name']): row['id'] for row in conn.execute("SELECT id, canonical_name FROM alchemy_entities").fetchall()}

    for chunk in chunks:
        text = chunk['text_clean']
        text_norm = normalize(text)
        
        for category, terms in lexicon.items():
            for term in terms:
                # Basic substring match for speed (Layer 1)
                # In production, you'd use a more robust matcher like spacy EntityRuler
                if term.lower() in text.lower():
                    norm_term = normalize(term)
                    
                    if norm_term in existing_entities:
                        entity_id = existing_entities[norm_term]
                    else:
                        entity_id = str(uuid.uuid4())
                        
                        # Historiographical Heuristics
                        h_tags = []
                        if category in ["ARTISANAL", "EQUIPMENT"]: h_tags.append("smith_artisanal")
                        if category in ["PROCESSES", "THEORIES"]: h_tags.append("principe_empirical")
                        if category == "ALLEGORIES": h_tags.append("traditional_hermetic")
                        
                        cursor.execute("""
                            INSERT INTO alchemy_entities (id, category, canonical_name, normalized_name, historiography_tags, run_id)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (entity_id, category, term, norm_term, json.dumps(h_tags), run_id))
                        existing_entities[norm_term] = entity_id
                        entities_mined += 1
                    
                    # Create mention
                    # Simple snippet extraction
                    start_idx = text.lower().find(term.lower())
                    snippet = text[max(0, start_idx - 50):min(len(text), start_idx + len(term) + 50)]
                    
                    cursor.execute("""
                        INSERT INTO alchemy_mentions (entity_id, chunk_id, document_id, context_snippet, confidence, method, run_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (entity_id, chunk['id'], chunk['document_id'], f"...{snippet}...", 0.9, "lexicon", run_id))
                    mentions_created += 1

    conn.commit()
    conn.close()
    print(f"Mining complete. New Entities: {entities_mined}, Mentions: {mentions_created}")

if __name__ == "__main__":
    # Ensure ingestion is done before running this
    mine_alchemy()
