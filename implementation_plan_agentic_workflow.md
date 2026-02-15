# Implementation Plan: V3 Agentic Designer Workflow

This plan transitions the "Renaissance Designer" team into a modular, agentic processing pipeline governed by a strict **Knowledge Graph Contract**. This ensures that historiographical interpretation is structured, queryable, and analytically sound.

## User Review Required
> [!IMPORTANT]
> This upgrade implements **SQLite Triggers** to enforce domain drift constraints. Relationships that violate the ontology will be hard-blocked at the database level.

## Proposed Changes

### 1. V3 Contract Schema Hardening
#### [NEW] [003_v3_contract_hardening.sql](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/migrations/003_v3_contract_hardening.sql)
- **ALCH_RUNS**: Update to UUID primary keys; add `run_type`, `status`, `git_commit`, `params_json`.
- **ALCH_ENTITIES**: Add `normalized_name` and `confidence` fields.
- **ALCH_ENTITY_ALIASES**: New table for entity convergence and provenance.
- **RELATIONSHIPS**: Add `source_chunk_id` and `evidence_snippet`.
- **PREDICATE_VOCAB**: Extend with `is_symmetric`, `requires_evidence`, `allowed_subject_domains`, `allowed_object_domains`.
- **TRIGGERS**:
    - `validate_relationship_domains`: Aborts insertion if subject/object domains are incompatible.
    - `validate_evidence_requirement`: Ensures evidence snippet is present for high-confidence analytical edges.

### 2. Designer Node Workflow
#### [MODIFY] [agentic_pipeline.py](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/agentic_pipeline.py)
- **State Machine**: Implement a DAG where each node accepts a `WorkflowState` and returns Pydantic-validated JSON.
- **Lawrence Node**: Logic for Allegory-to-Analog mapping with material phase detection.
- **Pamela Node**: Logic for Artisanal Context extraction (Labor verbs + Tool synergies).
- **Historiography Scorer**: Rule-based scoring for `principe_empirical`, `smith_artisanal`, and `traditional_hermetic`.

### 3. Pipeline Orchestration & Performance
#### [NEW] [run_v3_pipeline.py](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/run_v3_pipeline.py)
- **Relationship Buffer**: Accumulate extraction results in-memory, de-duplicate, and batch insert using single transactions for performance.
- **Rollback System**: Ensure every run can be perfectly reverted by `run_id` (UUID).

### 4. Hermetic Historiography Expansion
#### [NEW] [ingest_historiography.py](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/ingest_historiography.py)
- Ingest PDFs from `e:\pdf\hermetic`, `e:\pdf\ancient magic gnostic pgm etc`, `e:\pdf\Rosicrucian`, and `e:\pdf\crowley`.
- Map temporal layers using `historiography_tags`: `late_antique`, `medieval`, `renaissance`, `enlightenment`, `contemporary`.
- Populate `belongs_to_tradition` relationships for figures like Hermes Trismegistus, Paracelsus, Mead, etc.

### 5. Esoteric Image Vault
#### [NEW] [mine_images.py](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/mine_images.py)
- Extract images from PDFs using `fitz` (PyMuPDF).
- Store in `alchemy_images` table with metadata: `period`, `motif` (Dragon, Green Lion, Tree of Life, Seal), `category` (Emblem, Diagram, Illustration).
- Neighborhood cross-referencing: Link images to entities found in the same chunk.

### 6. Web & Archive Scraping
#### [NEW] [scrape_archives.py](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/scrape_archives.py)
- Targeted scraping of public domain alchemical image databases (e.g., alchemywebsite.com).
- Automated metadata tagging for extracted assets.

## Verification Plan

### Automated Tests
- `test_analytical_contract.py`: 
    - Assert that domain drift for Hermetic entities is blocked.
    - Verify that images are correctly anchored to source documents.
