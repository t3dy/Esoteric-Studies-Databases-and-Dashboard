import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

def add_column_if_not_exists(cursor, table, column, definition):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    if column not in columns:
        print(f"Adding column {column} to {table}...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
    else:
        print(f"Column {column} already exists in {table}.")

def run_v3_idempotent_migration():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tables check
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # 1. Predicate Vocabulary
    add_column_if_not_exists(cursor, "predicate_vocab", "is_symmetric", "BOOLEAN DEFAULT 0")
    add_column_if_not_exists(cursor, "predicate_vocab", "is_transitive", "BOOLEAN DEFAULT 0")
    add_column_if_not_exists(cursor, "predicate_vocab", "requires_evidence", "BOOLEAN DEFAULT 1")
    add_column_if_not_exists(cursor, "predicate_vocab", "allowed_subject_domains", "TEXT DEFAULT '[]'")
    add_column_if_not_exists(cursor, "predicate_vocab", "allowed_object_domains", "TEXT DEFAULT '[]'")
    
    # 2. Runs
    add_column_if_not_exists(cursor, "alchemy_runs", "run_uuid", "TEXT")
    add_column_if_not_exists(cursor, "alchemy_runs", "run_type", "TEXT")
    add_column_if_not_exists(cursor, "alchemy_runs", "status", "TEXT DEFAULT 'pending'")
    add_column_if_not_exists(cursor, "alchemy_runs", "params_json", "TEXT")
    add_column_if_not_exists(cursor, "alchemy_runs", "git_commit", "TEXT")
    
    # 3. Documents (for ingestion tracking)
    add_column_if_not_exists(cursor, "alchemy_documents", "file_hash", "TEXT") # Alias for sha256 or new column
    add_column_if_not_exists(cursor, "alchemy_documents", "domain", "TEXT")
    add_column_if_not_exists(cursor, "alchemy_documents", "run_id", "INTEGER REFERENCES alchemy_runs(id)")
    
    # 4. Entities
    add_column_if_not_exists(cursor, "alchemy_entities", "normalized_name", "TEXT")
    add_column_if_not_exists(cursor, "alchemy_entities", "confidence", "REAL DEFAULT 0.0")
    
    # 5. Relationships
    add_column_if_not_exists(cursor, "alchemy_relationships", "source_chunk_id", "INTEGER REFERENCES alchemy_chunks(id)")
    add_column_if_not_exists(cursor, "alchemy_relationships", "evidence_snippet", "TEXT")
    
    # 6. Mentions
    add_column_if_not_exists(cursor, "alchemy_mentions", "method", "TEXT DEFAULT 'regex'")
    add_column_if_not_exists(cursor, "alchemy_mentions", "weight", "REAL DEFAULT 1.0")
    
    # 7. Images (The Vault)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alchemy_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER REFERENCES alchemy_documents(id),
            page_number INTEGER,
            image_path TEXT,
            image_hash TEXT,
            caption TEXT,
            period TEXT, -- ancient, medieval, renaissance, etc.
            motif TEXT, -- animal, person, theory
            run_id INTEGER REFERENCES alchemy_runs(id),
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alchemy_entity_aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id TEXT REFERENCES alchemy_entities(id),
            alias TEXT,
            normalized_alias TEXT,
            source TEXT DEFAULT 'extracted',
            run_id INTEGER REFERENCES alchemy_runs(id)
        )
    """)
    
    # Predicates
    predicates = [
        ('analog_of', 'Symmetric mapping of allegory to reagent.', 'alchemy', 1, 1, '["alchemy"]', '["alchemy"]'),
        ('practiced_in', 'Relates a manual process to a workshop or guild context.', 'artisanal', 0, 1, '["process", "artisanal"]', '["artisanal"]'),
        ('artisan_of', 'Relates an individual to a specific craft.', 'artisanal', 0, 1, '["person"]', '["artisanal"]'),
        ('tool_used_in', 'Relates a tool/apparatus to a specific chemical process or experiment.', 'alchemy', 0, 1, '["tool"]', '["process"]'),
        ('belongs_to_tradition', 'Relates an entity to a specific reception layer.', 'historiography', 0, 1, '["scholar", "figure", "text"]', '["tradition"]')
    ]
    for p in predicates:
        cursor.execute("""
            INSERT OR IGNORE INTO predicate_vocab (predicate, description, domain, is_symmetric, requires_evidence, allowed_subject_domains, allowed_object_domains)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, p)
    
    # Triggers
    cursor.execute("DROP TRIGGER IF EXISTS validate_relationship_evidence_v3")
    cursor.execute("""
        CREATE TRIGGER validate_relationship_evidence_v3
        BEFORE INSERT ON alchemy_relationships
        FOR EACH ROW
        WHEN (SELECT requires_evidence FROM predicate_vocab WHERE predicate = NEW.predicate) = 1
        BEGIN
            SELECT CASE
                WHEN NEW.source_chunk_id IS NULL OR NEW.evidence_snippet IS NULL THEN
                    RAISE(ABORT, 'V3 Analytical Violation: This predicate requires source anchoring (source_chunk_id) and an evidence snippet.')
            END;
        END;
    """)
    
    conn.commit()
    conn.close()
    print("Idempotent V3 Migration Complete.")

if __name__ == "__main__":
    run_v3_idempotent_migration()
