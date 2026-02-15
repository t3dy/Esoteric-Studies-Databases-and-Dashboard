# V3 Engineering Plan: Engine Hardening & Cognition Stability

This plan shifts focus from thematic expansion to architectural professionalization. We are building the foundations for a **Corpus Intelligence Platform**.

## 1. Schema Sentinel (Migration Discipline)
- **Goal**: Deterministic database state across environments.
- **Components**:
    - `migrations/`: Directory for versioned SQL scripts.
    - `schema_version` table: Tracks applied versions.
    - `migrate.py`: Single entry point for DB updates.
- **Constraints**: 
    - PRAGMA foreign_keys = ON at connection time.
    - Startup schema validation check.

## 2. Relationship Weaver (Ontology Discipline)
- **Goal**: Transition from a document store to a Knowledge Graph.
- **Ontology**: Controlled vocabulary of predicates (mentions, influenced_by, analog_of).
- **Domain Isolation**: `domain` field in entities (alchemy, kabbalah, comics).

## 3. Reactive Event Bus (Reactive UI)
- **Goal**: Sub-second UI updates without polling.
- **Infrastructure**: FastAPI WebSockets + `events` table.
- **Events**: `ingestion_completed`, `mining_completed`, `schema_migrated`.

## 4. CI & Verification
- **GitHub Actions**: Automated linting (Ruff) and smoke testing.
- **Smoke Tests**: Verify API 200 codes, FK enforcement, and migration rollbacks.
- **Performance**: FTS5 search latency baseline.

## 5. Automated Documentation
- **Refactor Goal**: Generate `schema.md` and `api_docs.md` programmatically from DB reflection and FastAPI metadata.
- **Portfolio Integration**: Explanatory sections in README.md detailing Data Engineering and AI principles.

---

## 📅 Roadmap
### Sprint 1: Stability
1. Implement `schema_version` and `migrate.py`.
2. Apply `001_v3_core.sql` (Relationships + Predicates).
3. Setup WebSocket bus in `backend.py`.

### Sprint 2: Verification
1. Create `smoke_test.py`.
2. Implement Benchmarking script.
3. Update README to Portfolio Style.

### Sprint 3: Thematic Resumption
1. Add TMNT Relationship Graph.
2. Finalize Poetry Extraction with V3 Contracts.
