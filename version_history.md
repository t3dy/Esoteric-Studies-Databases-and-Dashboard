# Version History: Esoteric Knowledge System

This document outlines the evolution of the system from a prototype to a "Cognition Engine," detailing the problems solved and features enabled at each stage.

## Version 1.0.0: The Foundation (Initial Release)
**Focus**: Organization, Visibility, and Unified Deployment.

### Problem Solved
I started with a massive, unorganized collection of 1,600+ PDF files with messy names and hundreds of exported AI chat logs. The core problem was "Data Opacity"—knowing *that* I had a library, but not *what* was in it or how my own inquiry patterns were evolving.

### Key Features
- **Relational Ingestion**: Created a SQL database linking scholars, topics, and volumes.
- **Filename Sanitization (V1)**: Implemented aggressive regex cleaning to remove "bracketed noise" from filenames, making the file system human-readable for the first time.
- **The Popularity Contest**: Built a metrics-driven dashboard that visualizes which scholars were being referenced most frequently across 249 chats.
- **Unified Production Build**: Integrated the React frontend directly into the FastAPI backend so the user can launch a single service (`deploy_production.bat`) without needing complex dev environments.

### Why We Built It
We built V1 to solve the immediate paralysis of "Data Hoarding." By providing a visual dashboard, we enabled the user to see their research as a landscape rather than a directory list.

---

## Version 2.0.0: The Cognition Engine
**Focus**: Engineering Rigor, Reversibility, and High-Performance Search.

### Problem Solved
While V1 was visible, it wasn't robust. Aggressive renames couldn't be undone, scholar names were inconsistent (e.g., "Newton" vs. "Isaac Newton"), and searching through 10,000+ messages was slow. We transitioned from "Tool Building" to "Engineering."

### Key Features
- **Reversible Ingestion Pipeline**: Introduced `audit.db` and `rollback.py`. Every file mutation is now logged, allowing 100% data recovery if a regex rule is too aggressive.
- **Canonical Entity Resolution**: Replaced name-based linking with UUID-based IDs. This enables accurate "entity merging" where different spellings of a scholar link to the same canonical identity.
- **SQLite FTS5 Integration**: Migrated the search API to utilize virtual tables for full-text indexing. This enables sub-second search across the entire PDF/Chat corpus.
- **CS Architectural Lessons**: Codified the technical shifts into an educational document to help the user grow from a beginner to an architect.

### Why We Built It
V2 was built to enable "Refactoring at Scale." By ensuring every change is reversible and every scholar is uniquely identified, we created a system that can grow to 100k+ files without collapsing under its own technical debt. It solves the fear of "breaking the data" while adding the power of a professional research engine.
