# Implementation Plan: Alchemy Datamine & Knowledge Engine

Building a specialized extraction pipeline for the `/alchemy` corpus following the "Leonardo Protocol" for data integrity and provenance.

## 1. Data Model (SQLite)
We will expand the schema with dedicated tables for traceable entity extraction.

### Tables
- `alchemy_runs`: Tracks mining operations for easy rollback.
- `alchemy_entities`: Canonical storage for Alchemists, Materials, etc.
- `alchemy_mentions`: Links entities to specific text chunks/pages in PDFs.
- `alchemy_experiments`: Procedural data extracted from recipes.
- `alchemy_reconstructions`: Links modern replicate work (Principe) to historical sources.

## 2. Extraction Pipeline
### A. Ingestion (`ingest_alchemy_pdfs.py`)
- Scan `/alchemy` recursively.
- Extract per-page text (using `PyMuPDF`).
- Chunking (1000 tokens) with overlap and normalization.

### B. Mining (`mine_alchemy.py`)
- **Layer 1**: Lexicon-based seeding (Seeded lists for Processes/Equipment).
- **Layer 2**: NER (Names/Places) + Bibliographic heuristics.
- **Layer 3**: LLM-aided classification (Optional/Filtered) using retrieved context.

## 3. Dashboard Integration
### Alchemy Datamine View
- Category tabs (A-J).
- Evidence panels showing context snippets for every term.
- "Run History" management for triggers and rollbacks.

## 4. Alchemy Poetry Corpus
Building a specialized "Work-Level" database for alchemical verse.

### Data Model Expansion
- `alchemy_poems`: Canonical titles and metadata.
- `alchemy_poem_lines`: Lineated text preservation.
- `alchemy_witnesses`: Link to manuscript evidence (Ashmole, etc.).

### Extraction Strategy
1. **Pass 1: TOC Parsing**: Extracting spans from Schuler and Timmermann TOCs.
2. **Pass 2: Heading Heuristics**: Detecting verse markers (centered titles, stanza breaks).
3. **Pass 3: Line Normalization**: Preserving original lineation while providing search-normalized text.

## 5. Dashboard Integration
### Alchemy Portal Update
- **Category Tabs**: Added 'EXPERIMENTS' and 'RECONSTRUCTIONS'.
- **Poetry Tab**: Dedicated view for browsing canonical poems and their variants.
- **Evidence Panel**: 'Parchment' themed view focused on line-level provenance.

## 6. Verification Plan
### Functional Tests
- Idempotency: Re-ingesting poetry corpus skip existing documents.
- Search: FTS5 query for "Green Dragon" returns specific lines in poem context.
### Data Verification
- Verify poem boundaries against Schuler's annotated table of contents.
