# Engineering Plan: Esoteric Knowledge System (Version 2)

This plan moves the system from a prototype to a production-grade research platform.

## Goal: Version 2.0 (The Cognition Engine)
Transition from feature-hacking to a scalable, modular architecture with data reversibility and semantic depth.

## Phase 1: Infrastructure & Versioning
- **Git Strategy**: 
    - `main`: Production-ready code (Version 1 is tagged here).
    - `develop`: Ongoing synthesis.
    - `feature/*`: Isolated branches for new modules (e.g., `feature/entity-resolution`, `feature/fts5-search`).
- **Database Migrations**: Implement a versioned migration folder (`/migrations`) containing SQL scripts for schema updates. This replaces manual `cursor.execute` calls in Python.

## Phase 2: Reversible Ingestion Pipeline
- **Separation of Concerns**: 
    - `raw/`: Immutable original files.
    - `processed/`: Current system state.
- **The Audit System**: Every file operation (like renaming) will write to a `metadata_audit.db` before execution.
- **Rollback Tool**: A Python script `rollback.py` that reads the audit log and can undo the last $N$ operations.

## Phase 3: Entity Resolution & Knowledge Graph
- **Normalization Engine**: Build a script that scans the `entities` table to disambiguate scholars.
- **Graph Visualization**: Transition the "Scholars" list into a network graph showing overlapping mentions across different chats.

## Phase 4: Scalability & Full-Text Search
- **FTS5 Integration**: Migrate the existing `search` logic from `LIKE %search%` queries to an SQLite FTS5 index for ranking and faster retrieval across 10k+ rows of chat content.
- **Postgres Readiness**: Ensure all SQLAlchemy/Python logic is "DB agnostic," allowing us to migrate to PostgreSQL if the library exceeds 10GB.

## Phase 5: Testing & Reliability
- **Verification Suite**: Add a `tests/` directory with `pytest` for:
    - Ingestion logic (parentheses removal).
    - Schema integrity (foreign key constraints).
    - API endpoint uptime.

---

## User Review Required
> [!IMPORTANT]
> **Branching Strategy**: I recommend shifting all current V1 files into a "v1-legacy" branch or folder if we intend to radically change the directory structure in V2. 
> **Data Reversibility**: Do you want the `rollback.csv` to be kept indefinitely, or rotate it after a certain period?
