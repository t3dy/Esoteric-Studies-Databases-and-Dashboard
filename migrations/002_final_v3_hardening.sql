-- Migration 002: V3 Analytical Contract (Consolidated)
-- Goal: Transform the database into a strict, auditable Knowledge Graph with analytical grounding.

-- 1. Predicate Vocabulary Hardening
ALTER TABLE predicate_vocab ADD COLUMN is_symmetric BOOLEAN DEFAULT 0;
ALTER TABLE predicate_vocab ADD COLUMN is_transitive BOOLEAN DEFAULT 0;
ALTER TABLE predicate_vocab ADD COLUMN requires_evidence BOOLEAN DEFAULT 1;
ALTER TABLE predicate_vocab ADD COLUMN allowed_subject_domains TEXT DEFAULT '[]'; -- JSON Array
ALTER TABLE predicate_vocab ADD COLUMN allowed_object_domains TEXT DEFAULT '[]';  -- JSON Array

-- 2. New Artisanal & Analytical Predicates
INSERT OR IGNORE INTO predicate_vocab (predicate, description, domain, is_symmetric, requires_evidence, allowed_subject_domains, allowed_object_domains) VALUES
('analog_of', 'Symmetric mapping of allegory to reagent.', 'alchemy', 1, 1, '["alchemy"]', '["alchemy"]'),
('practiced_in', 'Relates a manual process to a workshop or guild context.', 'artisanal', 0, 1, '["process", "artisanal"]', '["artisanal"]'),
('artisan_of', 'Relates an individual to a specific craft.', 'artisanal', 0, 1, '["person"]', '["artisanal"]'),
('tool_used_in', 'Relates a tool/apparatus to a specific chemical process or experiment.', 'alchemy', 0, 1, '["tool"]', '["process"]'),
('belongs_to_tradition', 'Relates an entity to a specific reception layer (e.g., Late Antique, Renaissance).', 'historiography', 0, 1, '["scholar", "figure", "text"]', '["tradition"]');

-- 3. Run Metadata (UUID-logical identity)
ALTER TABLE alchemy_runs ADD COLUMN run_uuid TEXT;
ALTER TABLE alchemy_runs ADD COLUMN run_type TEXT; -- ingest | datamine | relink | merge | migrate
ALTER TABLE alchemy_runs ADD COLUMN status TEXT DEFAULT 'pending';

-- 4. Entity Convergence (Aliases)
CREATE TABLE IF NOT EXISTS alchemy_entity_aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT REFERENCES alchemy_entities(id),
    alias TEXT,
    normalized_alias TEXT,
    source TEXT DEFAULT 'extracted', -- extracted | manual | imported
    run_id INTEGER REFERENCES alchemy_runs(id)
);

-- 5. Relationship Anchoring & Grounding
ALTER TABLE alchemy_relationships ADD COLUMN source_chunk_id INTEGER REFERENCES alchemy_chunks(id);
ALTER TABLE alchemy_relationships ADD COLUMN evidence_snippet TEXT;

-- 6. Mentions Depth
ALTER TABLE alchemy_mentions ADD COLUMN method TEXT DEFAULT 'regex'; -- regex | ner | llm | rule | manual
ALTER TABLE alchemy_mentions ADD COLUMN weight REAL DEFAULT 1.0;

-- 7. High-Performance Indices
CREATE INDEX IF NOT EXISTS idx_rel_subject ON alchemy_relationships(subject_entity_id, predicate);
CREATE INDEX IF NOT EXISTS idx_rel_object ON alchemy_relationships(object_entity_id, predicate);
CREATE INDEX IF NOT EXISTS idx_mentions_entity ON alchemy_mentions(entity_id);
CREATE INDEX IF NOT EXISTS idx_mentions_chunk ON alchemy_mentions(chunk_id);

-- 8. Domain Enforcement Trigger
CREATE TRIGGER IF NOT EXISTS validate_relationship_evidence_v3
BEFORE INSERT ON alchemy_relationships
FOR EACH ROW
WHEN (SELECT requires_evidence FROM predicate_vocab WHERE predicate = NEW.predicate) = 1
BEGIN
    SELECT CASE
        WHEN NEW.source_chunk_id IS NULL OR NEW.evidence_snippet IS NULL THEN
            RAISE(ABORT, 'V3 Analytical Violation: This predicate requires source anchoring (source_chunk_id) and an evidence snippet.')
    END;
END;
