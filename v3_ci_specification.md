# V3 CI Pipeline & Test Suite Specification

To maintain a "Production-Grade" archive, we are implementing a **Rigorous Verification Layer**.

## 1. CI Pipeline (GitHub Actions)
```yaml
name: Cognition Engine V3 CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install Base Deps
        run: pip install fastapi uvicorn pytest
      - name: Run Migrations
        run: python migrate.py
      - name: Execute Smoke Tests
        run: python smoke_test.py
      - name: Run Schema Validator
        run: python validate_schema.py
```

## 2. Test Suite Components

### A. Migration Invariant Tests (`test_migrations.py`)
- **Forward Progress**: Assert that applying migrations results in the correct version in `schema_version`.
- **Integrity**: Attempt to insert a row with a missing Foreign Key (should fail).
- **Idempotency**: Running `migrate.py` twice should have no effect on the database state.

### B. Ingestion Contract Tests (`test_ingestion.py`)
- **Hash Stability**: Assert that re-ingesting the same file results in zero new document rows.
- **Chunk Anchoring**: Verify that chunk offsets correctly map to the raw text in a sample PDF.

### C. Relationship Ontology Tests (`test_ontology.py`)
- **Predicate Validation**: Attempting to insert a relationship with a predicate NOT in `predicate_vocab` must raise an error.
- **Inverse Integrity**: Verify that triggering an `influenced_by` link correctly suggests or creates the `influenced` inverse (Planned for V3.1).

## 3. Performance Benchmarking
A weekly cron job will run `benchmark_search.py` to ensure that FTS5 search latency remains < 100ms for common terms as the corpus scales to 1,000,000 chunks.
