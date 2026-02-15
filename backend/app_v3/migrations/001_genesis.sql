-- V3 Genesis Schema: The Contract
-- STRICT PROVENANCE, ONTOLOGY DISCIPLINE, REVERSIBILITY

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- 1. Schema Versioning (The Gatekeeper)
CREATE TABLE IF NOT EXISTS schema_version (
    version_number INTEGER PRIMARY KEY,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL
);

-- 2. Runs (The Unit of Reversibility)
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY, -- UUID
    run_type TEXT NOT NULL, -- 'import', 'mining', 'manual', 'migration'
    params_json TEXT,
    git_commit TEXT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME,
    status TEXT CHECK(status IN ('running', 'success', 'failed', 'rolled_back')),
    notes TEXT
);

-- 3. File Manifest (The Anchor)
CREATE TABLE IF NOT EXISTS file_manifest (
    file_hash TEXT PRIMARY KEY, -- SHA256 of file content
    current_path TEXT NOT NULL,
    logical_collection TEXT, -- 'library', 'chats', 'archive'
    first_seen_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    status TEXT CHECK(status IN ('active', 'missing', 'moved'))
);

-- 4. Documents (The Corpus)
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY, -- UUID
    file_hash TEXT REFERENCES file_manifest(file_hash),
    title TEXT NOT NULL,
    doc_type TEXT NOT NULL DEFAULT 'primary', -- 'primary', 'commentary', 'chat_log'
    domain TEXT, -- 'alchemy', 'hermetic', 'rosicrucian'
    language TEXT,
    publication_date TEXT,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    run_id TEXT REFERENCES runs(id)
);

-- 5. Chunks (The Evidence Source)
CREATE TABLE IF NOT EXISTS chunks (
    id TEXT PRIMARY KEY, -- UUID
    document_id TEXT REFERENCES documents(id) ON DELETE CASCADE,
    page_start INTEGER,
    page_end INTEGER,
    text_clean TEXT NOT NULL,
    text_raw TEXT, -- Optional preservation
    extraction_version TEXT, -- 'v1-pymupdf', 'v2-layoutlm'
    run_id TEXT REFERENCES runs(id)
);

-- 6. Entities (Canonical Identities)
CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY, -- UUID
    canonical_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL, -- lowercase, ascii only
    category TEXT NOT NULL CHECK(category IN ('ALCHEMIST', 'CONCEPT', 'PROCESS', 'MATERIAL', 'LOCATION', 'TEXT')),
    domain TEXT,
    description TEXT,
    confidence REAL DEFAULT 1.0,
    historiography_tags JSON, -- '{"hermetic": 0.9, "scientific": 0.1}'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    run_id TEXT REFERENCES runs(id)
);

-- 7. Entity Aliases (Resolution)
CREATE TABLE IF NOT EXISTS entity_aliases (
    id TEXT PRIMARY KEY, -- UUID
    entity_id TEXT REFERENCES entities(id) ON DELETE CASCADE,
    alias TEXT NOT NULL,
    source TEXT, -- 'manual', 'llm-merge', 'regex'
    run_id TEXT REFERENCES runs(id)
);

-- 8. Predicate Vocabulary (The Ontology)
-- Enforced via triggers on relationships table
CREATE TABLE IF NOT EXISTS predicate_vocab (
    predicate TEXT PRIMARY KEY,
    description TEXT,
    is_symmetric BOOLEAN DEFAULT 0,
    allowed_subject_domains JSON, -- '["alchemy", "any"]'
    allowed_object_domains JSON
);

-- Seed Predicates
INSERT INTO predicate_vocab (predicate, description, is_symmetric) VALUES 
('influenced_by', 'Subject was influenced by Object', 0),
('analog_of', 'Subject is symbolically equivalent to Object', 1),
('member_of', 'Subject is part of Object group', 0),
('author_of', 'Subject wrote Object', 0),
('mentions', 'Subject text mentions Object entity', 0);

-- 9. Relationships (The Graph)
CREATE TABLE IF NOT EXISTS relationships (
    id TEXT PRIMARY KEY, -- UUID
    subject_entity_id TEXT REFERENCES entities(id) ON DELETE CASCADE,
    predicate TEXT REFERENCES predicate_vocab(predicate),
    object_entity_id TEXT REFERENCES entities(id) ON DELETE CASCADE,
    evidence_chunk_id TEXT REFERENCES chunks(id), -- Nullable only if manual
    evidence_snippet TEXT,
    confidence REAL DEFAULT 0.5,
    run_id TEXT REFERENCES runs(id)
);

-- 10. Mentions (The Index)
CREATE TABLE IF NOT EXISTS mentions (
    id TEXT PRIMARY KEY, -- UUID
    entity_id TEXT REFERENCES entities(id) ON DELETE CASCADE,
    chunk_id TEXT REFERENCES chunks(id) ON DELETE CASCADE,
    document_id TEXT REFERENCES documents(id), -- Denormalized for speed
    context_snippet TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    run_id TEXT REFERENCES runs(id)
);

-- 11. Mining Log (Observability)
CREATE TABLE IF NOT EXISTS mining_log (
    id TEXT PRIMARY KEY, -- UUID
    run_id TEXT REFERENCES runs(id),
    agent_id TEXT, -- 'Lawrence', 'Pamela', 'Scanner'
    action_type TEXT, -- 'extract_entity', 'infer_relation', 'score_hist'
    target_id TEXT, -- Entity/Doc ID affected
    payload_json TEXT, -- Full details
    confidence REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TRIGGERS & ENFORCEMENT

-- Trigger: Prevent relationships with invalid predicates (Redundant via FK but good for errors)
CREATE TRIGGER IF NOT EXISTS validate_predicate
BEFORE INSERT ON relationships
BEGIN
    SELECT CASE 
        WHEN (SELECT 1 FROM predicate_vocab WHERE predicate = NEW.predicate) IS NULL
        THEN RAISE(ABORT, 'Invalid Predicate: Not in Vocabulary')
    END;
END;

-- V3 Initial Schema Applied
INSERT INTO schema_version (version_number, description) VALUES (1, 'V3 Genesis: Contract First');
