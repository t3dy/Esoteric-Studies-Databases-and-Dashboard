# Schema Design: Esoteric Knowledge System (V2)

This document formalizes the data contract for Version 2. It shifts from name-based links to a **Canonical Entity ID** model.

## 1. Entities & Scholars
### Table: `entities`
*Primary source of truth for scholars, authors, and historical figures.*
- `id`: UUID (Primary Key)
- `canonical_name`: TEXT (Unique, e.g., "Pico della Mirandola")
- `normalized_name`: TEXT (Lowercase ASCII for searching)
- `category`: TEXT (e.g., "scholar", "alchemist", "critic")
- `metadata`: JSON (Dates, locations, alternate spellings)

### Table: `entity_mentions`
*Stores every time an entity is mentioned in a chat or volume.*
- `id`: INTEGER (PK)
- `entity_id`: UUID (FK -> entities.id)
- `source_type`: TEXT ('chat', 'title', 'media')
- `source_id`: INTEGER (FK)
- `confidence`: FLOAT (Success rate of resolution)

## 2. The Library (Volumes)
### Table: `volumes`
- `id`: INTEGER (PK)
- `title`: TEXT
- `original_filename`: TEXT (Crucial for reversibility)
- `path`: TEXT (Relative)
- `category_id`: INTEGER (FK)
- `hash`: TEXT (SHA256 of file content to detect duplicates)
- `summary`: TEXT

## 3. The Knowledge Archive (Chats)
### Table: `chats`
- `id`: INTEGER (PK)
- `title`: TEXT
- `date_created`: TIMESTAMP
- `model`: TEXT
- `msg_count`: INTEGER
- `folder_path`: TEXT

### Table: `questions`
- `id`: INTEGER (PK)
- `chat_id`: INTEGER (FK)
- `text`: TEXT
- `move_type`: TEXT (Indexed)
- `intent_score`: FLOAT

## 4. Reversibility & Logs
### Table: `audit_log`
*Records every destructive mutation (rename, delete, merge).*
- `id`: INTEGER (PK)
- `timestamp`: TIMESTAMP
- `operation`: TEXT (e.g., 'RENAME')
- `target_type`: TEXT ('volume', 'entity')
- `target_id`: INTEGER
- `pre_state`: JSON (The "before" data)
- `post_state`: JSON (The "after" data)

## 5. Indexing & Optimization
- **FTS5 Virtual Table**: `volumes_fts` and `chats_fts` for sub-second search across titles and message content.
- **Indices**:
    - `idx_entity_name` on `entities.normalized_name`
    - `idx_question_move` on `questions.move_type`
    - `idx_volume_hash` on `volumes.hash`
