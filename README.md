# 🚀 Research Cognition Engine: V3 Release
**Status:** Live (GitHub Pages) | **Version:** 3.0.0
<!-- Force Rebuild -->

## 🔗 Quick Access (NEW: Zero-Config)
These links work immediately in your browser. No installation required.

| Resource | URL | Status |
| :--- | :--- | :--- |
| **Hosted Dashboard** | **[Live Dashboard](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/)** | ✅ **Active** (Static Snapshot) |
| **Hosted Manuals** | **[Documentation Hub](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/docs/index.html)** | ✅ **Active** (Guides & Reports) |
| **GitHub Repository** | **[Source Code](https://github.com/t3dy/Esoteric-Studies-Databases-and-Dashboard)** | ✅ **Active** |

## 🔄 How to Update the Data (Local Publisher)
To update the data shown on the hosted dashboard:
1. Run `./publish.ps1` in PowerShell.
2. Wait ~60 seconds for GitHub to deploy.

## ⚠️ Legacy Local Links (Developer Mode)
*Note: The following links **DO NOT WORK** unless you are running the local Python engine (`uvicorn`). They are for development only.*

| Legacy Component | Local URL | Status |
| :--- | :--- | :--- |
| **V3 Image Vault** | `http://localhost:5173/gallery` | ❌ **Offline** (Requires `npm run dev`) |
| **V3 Alchemy Portal** | `http://localhost:5173/alchemy` | ❌ **Offline** (Requires `npm run dev`) |
| **V2 Knowledge Graph** | `http://localhost:5173?view=knowledge` | ❌ **Offline** (Requires `npm run dev`) |
| **V1 Archive** | `http://localhost:5173?view=library` | ❌ **Offline** (Requires `npm run dev`) |

### 📄 Critiques & Reports
- **[Prompt Engineering Critique](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/docs/viewer.html?doc=prompt_engineering_critique.md)**
- **[Analysis Report](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/docs/viewer.html?doc=analysis_report.md)**

# Research Cognition Engine: A Data Engineering Portfolio
**CS & AI Engineering Showcase**

Welcome to the **Research Cognition Engine**—a multi-layered data pipeline designed to transform fragmented PDF archives and esoteric chat logs into a structured, high-fidelity Knowledge Graph. This project serves as a practical application of advanced Computer Science and AI Engineering principles.

## 🚀 Architectural Vision: Cascading Integration
Unlike basic storage systems, this engine employs a **Cascading Update** architecture. Every file is uniquely identified by its SHA256 hash, making the system resilient to path changes and duplicates.

### 🛠️ Data Engineering Concepts Applied
- **Deterministic Ingestion**: Using hash-based identity to ensure 100% data integrity during migration and renaming.
- **Relational Integrity (Schema Sentinel)**: A custom migration engine ([migrate.py](https://github.com/t3dy/Esoteric-Studies-Databases-and-Dashboard/blob/main/backend/app_v3/migrate.py)) manages the evolution of the SQLite schema, enforcing strict foreign key constraints.
- **Micro-Chunking & Anchoring**: Documents are discretized into semantic chunks, anchored to character offsets for sub-page provenance tracking.

### 🧠 AI & Knowledge Sovereignty
- **Lexical Mining (NER)**: A hybrid Named Entity Recognition engine used to extract thousands of Alchemical, Kabbalistic, and Historiographical entities.
- **Ontology Discipline (Relationship Weaver)**: The move from a "bucket of tags" to a "Knowledge Graph" using controlled predicates like `influenced_by` and `analog_of`.
- **FTS5 Search**: High-performance Full-Text Search integration for millisecond retrieval across hundreds of thousands of textual tokens.

## 📈 System Maturity (V3 Hardening)
- **Local-First Architecture**: V3 operates on a "Publish-to-Static" model, ensuring dashboards are always available without fragile backend dependencies.
- **CI/CD Pipeline**: Automated smoke tests and benchmarking for search latency.
- **Audit Stability**: 100% reversible operations via the Audit & Rollback module.

---
*Created as a capstone exploration in Data Engineering and AI-assisted knowledge management.*
