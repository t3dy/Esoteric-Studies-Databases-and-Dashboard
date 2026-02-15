-- Alchemy Knowledge Schema Migration (Improved for Traceability)
-- Force reset for development (uncomment if needed, but here we use it to fix column mismatch)
DROP TABLE IF EXISTS alchemy_poetry_fts;
DROP TABLE IF EXISTS alchemy_poem_lines;
DROP TABLE IF EXISTS alchemy_poem_spans;
DROP TABLE IF EXISTS alchemy_poem_sources;
DROP TABLE IF EXISTS alchemy_poems;
DROP TABLE IF EXISTS alchemy_witnesses;
DROP TABLE IF EXISTS alchemy_relationships;
DROP TABLE IF EXISTS alchemy_mentions;
DROP TABLE IF EXISTS alchemy_entities;
DROP TABLE IF EXISTS alchemy_entity_aliases;
-- Note: alchemy_runs/documents/pages/chunks are usually safer to keep, but if column mismatch persists:
-- DROP TABLE IF EXISTS alchemy_chunks; 

-- Table: alchemy_runs (Traceability/Rollback)
CREATE TABLE IF NOT EXISTS alchemy_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME,
    params_json TEXT,
    git_commit TEXT,
    notes TEXT
);

-- Table: alchemy_documents (Source Tracking)
CREATE TABLE IF NOT EXISTS alchemy_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    title TEXT,
    folder TEXT,
    sha256 TEXT,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: alchemy_pages (Page-level text)
CREATE TABLE IF NOT EXISTS alchemy_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    page_no INTEGER,
    text_raw TEXT,
    FOREIGN KEY(document_id) REFERENCES alchemy_documents(id)
);

-- Table: alchemy_chunks (Atomic units for mining)
CREATE TABLE IF NOT EXISTS alchemy_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    page_start INTEGER,
    page_end INTEGER,
    text_clean TEXT,
    char_start INTEGER,
    char_end INTEGER,
    sha256 TEXT,
    FOREIGN KEY(document_id) REFERENCES alchemy_documents(id)
);

-- Table: alchemy_entities (Canonical Facts)
CREATE TABLE IF NOT EXISTS alchemy_entities (
    id TEXT PRIMARY KEY, -- UUID
    category TEXT NOT NULL, -- A-J + New (Allegory, Image, Artisanal)
    canonical_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    metadata_json TEXT, -- Short definition, confidence, etc.
    historiography_tags TEXT, -- JSON: ["Principe", "Smith", "Traditional"]
    material_alignment TEXT, -- JSON linking to artisanal practices
    run_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(run_id) REFERENCES alchemy_runs(id)
);

-- Table: alchemy_entity_aliases
CREATE TABLE IF NOT EXISTS alchemy_entity_aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT,
    alias TEXT NOT NULL,
    normalized_alias TEXT NOT NULL,
    FOREIGN KEY(entity_id) REFERENCES alchemy_entities(id)
);

-- Table: alchemy_mentions (Provenance Link)
CREATE TABLE IF NOT EXISTS alchemy_mentions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT,
    chunk_id INTEGER,
    document_id INTEGER,
    page_hint INTEGER,
    context_snippet TEXT,
    confidence REAL,
    method TEXT,
    run_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(entity_id) REFERENCES alchemy_entities(id),
    FOREIGN KEY(chunk_id) REFERENCES alchemy_chunks(id),
    FOREIGN KEY(document_id) REFERENCES alchemy_documents(id),
    FOREIGN KEY(run_id) REFERENCES alchemy_runs(id)
);

-- Table: alchemy_relationships
CREATE TABLE IF NOT EXISTS alchemy_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_entity_id TEXT,
    predicate TEXT,
    object_entity_id TEXT,
    chunk_id INTEGER,
    confidence REAL,
    FOREIGN KEY(subject_entity_id) REFERENCES alchemy_entities(id),
    FOREIGN KEY(object_entity_id) REFERENCES alchemy_entities(id),
    FOREIGN KEY(chunk_id) REFERENCES alchemy_chunks(id)
);

-- Create Indices
CREATE INDEX IF NOT EXISTS idx_alchemy_entities_cat ON alchemy_entities(category);
CREATE INDEX IF NOT EXISTS idx_alchemy_chunks_doc ON alchemy_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_alchemy_mentions_entity ON alchemy_mentions(entity_id);
CREATE INDEX IF NOT EXISTS idx_alchemy_mentions_chunk ON alchemy_mentions(chunk_id);

-- --- Alchemy Poetry Corpus Tables ---

-- Table: alchemy_poems (The canonical work)
CREATE TABLE IF NOT EXISTS alchemy_poems (
    id TEXT PRIMARY KEY, -- UUID
    canonical_title TEXT NOT NULL,
    incipit TEXT,
    explicit TEXT,
    language TEXT,
    date_range TEXT,
    genre_tags TEXT, -- JSON
    alchemy_tags TEXT, -- JSON
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: alchemy_poem_sources (Relationship between a poem and a PDF edition)
CREATE TABLE IF NOT EXISTS alchemy_poem_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poem_id TEXT,
    document_id INTEGER,
    source_type TEXT, -- edition | translation | anthology
    editor_author TEXT,
    citation TEXT,
    rights_limit TEXT, -- public | snippet_only
    FOREIGN KEY(poem_id) REFERENCES alchemy_poems(id),
    FOREIGN KEY(document_id) REFERENCES alchemy_documents(id)
);

-- Table: alchemy_poem_spans (Page ranges in a PDF)
CREATE TABLE IF NOT EXISTS alchemy_poem_spans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poem_source_id INTEGER,
    page_start INTEGER,
    page_end INTEGER,
    method TEXT, -- toc | heuristic | manual
    FOREIGN KEY(poem_source_id) REFERENCES alchemy_poem_sources(id)
);

-- Table: alchemy_poem_lines (Atomic line data)
CREATE TABLE IF NOT EXISTS alchemy_poem_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poem_id TEXT,
    poem_source_id INTEGER,
    line_no INTEGER,
    line_text_raw TEXT,
    line_text_norm TEXT,
    page_no_hint INTEGER,
    FOREIGN KEY(poem_id) REFERENCES alchemy_poems(id),
    FOREIGN KEY(poem_source_id) REFERENCES alchemy_poem_sources(id)
);

-- Table: alchemy_witnesses (Manuscript records)
CREATE TABLE IF NOT EXISTS alchemy_witnesses (
    id TEXT PRIMARY KEY,
    poem_id TEXT,
    shelfmark TEXT,
    repository TEXT,
    date_est TEXT,
    notes TEXT,
    FOREIGN KEY(poem_id) REFERENCES alchemy_poems(id)
);

-- FTS5 Table for Poetry Search
CREATE VIRTUAL TABLE IF NOT EXISTS alchemy_poetry_fts USING fts5(
    poem_id UNINDEXED,
    line_text_norm,
    content='alchemy_poem_lines',
    content_rowid='id'
);
