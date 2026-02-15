# V3 Knowledge Graph: ER Diagram & Ontology Spec

## 1. Unified Entity-Relationship Model (Mermaid)

```mermaid
erDiagram
    ALCH_RUNS ||--o{ ALCH_DOCS : "contains"
    ALCH_DOCS ||--o{ ALCH_PAGES : "has"
    ALCH_PAGES ||--o{ ALCH_CHUNKS : "segments"
    ALCH_CHUNKS ||--o{ ALCH_MENTIONS : "anchors"
    ALCH_ENTITIES ||--o{ ALCH_MENTIONS : "referenced_in"
    ALCH_ENTITIES ||--o{ RELATIONSHIPS : "subject_of"
    ALCH_ENTITIES ||--o{ RELATIONSHIPS : "object_of"
    PREDICATE_VOCAB ||--o{ RELATIONSHIPS : "defines"
    SCHEMA_VERSION ||--o{ ALCH_RUNS : "validates"

    ALCH_ENTITIES {
        string id PK
        string category
        string canonical_name
        string domain
        json historiography_tags
        json material_alignment
    }

    RELATIONSHIPS {
        string id PK
        string subject_entity_id FK
        string predicate FK
        string object_entity_id FK
        float confidence
        int run_id FK
    }

    PREDICATE_VOCAB {
        string predicate PK
        string description
        string domain
        string inverse_predicate
    }
```

## 2. Controlled Predicate Ontology

| Predicate | Description | Domain | Inverse |
| :--- | :--- | :--- | :--- |
| `mentions` | Basic textual reference to an entity. | general | `mentioned_by` |
| `influenced_by` | Creative or intellectual lineage. | general | `influenced` |
| `analog_of` | Symbolic or chemical correspondence (e.g., Sun -> Gold). | alchemy | `analog_of` |
| `member_of` | Group/Guild membership (Artisanal context). | general | `has_member` |
| `uses_tool` | Connection between alchemist and apparatus. | alchemy | `tool_used_by` |
| `reconstruction_of` | Modern laboratory replication of a historic recipe. | alchemy | `source_for_reconstruction` |

## 3. Structural Soundness & Fragility Audit

### Structural Soundness
- **Hash-Anchored Chunking**: Prevents data loss during file moves.
- **Migration Registry**: Ensures all nodes in a cluster (or future distributed dev environments) share a consistent schema.

### Hidden Fragilities
- **Predicate Ambiguity**: Without the `predicate_vocab` check, users might create redundant predicates (e.g., `part_of` vs `member_of`).
- **Domain Drift**: We must enforce that an entity in the `comics` domain cannot have an `analog_of` relationship with an `alchemy` process unless explicitly whitelisted.
- **SQLite Locking**: High-velocity Relationship extraction (The "Loom") may hit write-contention. We should implement a "Relationship Buffer" in-memory before batch inserting.
