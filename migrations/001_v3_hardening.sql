-- Migration 001: V3 Hardening & Infrastructure
-- Target: library.db

-- Table: schema_version (The Source of Truth for DB state)
CREATE TABLE IF NOT EXISTS schema_version (
    version_number INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    git_commit TEXT
);

-- Table: predicate_vocab (Controlled Ontology)
CREATE TABLE IF NOT EXISTS predicate_vocab (
    predicate TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    domain TEXT DEFAULT 'general',
    inverse_predicate TEXT
);

-- Seed Predicates
INSERT OR IGNORE INTO predicate_vocab (predicate, description, domain) VALUES 
('mentions', 'Basic textual reference', 'general'),
('influenced_by', 'Intellectual or creative influence', 'general'),
('analog_of', 'Conceptual or chemical correspondence', 'alchemy'),
('reconstruction_of', 'Modern laboratory replication of historic work', 'alchemy'),
('thematic_overlap', 'Significant shared themes', 'general'),
('citation_reference', 'Formal academic citation', 'general');

-- Table: relationships (Knowledge Graph)
CREATE TABLE IF NOT EXISTS relationships (
    id TEXT PRIMARY KEY,
    subject_entity_id TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object_entity_id TEXT NOT NULL,
    source_chunk_id INTEGER,
    confidence REAL DEFAULT 1.0,
    run_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(subject_entity_id) REFERENCES alchemy_entities(id),
    FOREIGN KEY(object_entity_id) REFERENCES alchemy_entities(id),
    FOREIGN KEY(source_chunk_id) REFERENCES alchemy_chunks(id),
    FOREIGN KEY(predicate) REFERENCES predicate_vocab(predicate)
);

-- Table: events (Reactive Bus)
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Add extraction_version to chunks (Schema Patch)
-- Note: SQLite doesn't support IF NOT EXISTS in ALTER TABLE
-- We will handle this in the migrate.py logic or just try/except

-- Record this migration
INSERT INTO schema_version (version_number, description) VALUES (1, 'V3 Hardening: Ontology, Relationships, and Events');
