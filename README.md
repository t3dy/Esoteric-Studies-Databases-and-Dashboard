# 🚀 Research Cognition Engine: V3 Release
**Status:** Live (Local) | **Version:** 3.0.0 | **Commit:** `HEAD`

## 🔗 Quick Access
| Resource | URL | Version / Role |
| :--- | :--- | :--- |
| **GitHub Repository** | **[Esoteric-Studies-Databases-and-Dashboard](https://github.com/t3dy/Esoteric-Studies-Databases-and-Dashboard)** | Source Code & Version Control |
| **Documentation Hub** | **[http://localhost:5173/docs/index.html](http://localhost:5173/docs/index.html)** | Guides (V1/V2/V3) & Reports Viewer |
| **V3 Dashboard** | **[http://localhost:5173](http://localhost:5173)** | **Current Production** (Includes V1/V2 Features) |

## 🖥️ System Versions & Entry Points
The V3 Dashboard unifies all previous versions. Use these links to access specific historical modes:

| Version | Interface Name | Direct Link | Description |
| :--- | :--- | :--- | :--- |
| **V3** | **The Image Vault** | [http://localhost:5173/gallery](http://localhost:5173/gallery) | The "Mutus Liber" Gallery (New!) |
| **V3** | **Alchemy Portal** | [http://localhost:5173/alchemy](http://localhost:5173/alchemy) | Entity Mining & Knowledge Graph |
| **V2** | **The Graph** | [http://localhost:5173?view=knowledge](http://localhost:5173?view=knowledge) | Scholar/Concept Analysis (Legacy V2 View) |
| **V1** | **The Archive** | [http://localhost:5173?view=library](http://localhost:5173?view=library) | PDF Library & Metadata (Legacy V1 View) |

### 📄 Key Reports & Artifacts
- **[Analysis Report](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/analysis_report.md)**: System Audit.
- **[Doctumentation Plan](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/documentation_plan.md)**: Deployment Strategy.

# Research Cognition Engine: A Data Engineering Portfolio
**CS & AI Engineering Showcase**

Welcome to the **Research Cognition Engine**—a multi-layered data pipeline designed to transform fragmented PDF archives and esoteric chat logs into a structured, high-fidelity Knowledge Graph. This project serves as a practical application of advanced Computer Science and AI Engineering principles.

## 🚀 Architectural Vision: Cascading Integration
Unlike basic storage systems, this engine employs a **Cascading Update** architecture. Every file is uniquely identified by its SHA256 hash, making the system resilient to path changes and duplicates.

### 🛠️ Data Engineering Concepts Applied
- **Deterministic Ingestion**: Using hash-based identity to ensure 100% data integrity during migration and renaming.
- **Relational Integrity (Schema Sentinel)**: A custom migration engine ([migrate.py](file:///C:/Users/PC/.gemini/antigravity/brain/36954c62-9d67-4848-94a4-278b6cac4051/migrate.py)) manages the evolution of the SQLite schema, enforcing strict foreign key constraints.
- **Micro-Chunking & Anchoring**: Documents are discretized into semantic chunks, anchored to character offsets for sub-page provenance tracking.

### 🧠 AI & Knowledge Sovereignty
- **Lexical Mining (NER)**: A hybrid Named Entity Recognition engine used to extract thousands of Alchemical, Kabbalistic, and Historiographical entities.
- **Ontology Discipline (Relationship Weaver)**: The move from a "bucket of tags" to a "Knowledge Graph" using controlled predicates like `influenced_by` and `analog_of`.
- **FTS5 Search**: High-performance Full-Text Search integration for millisecond retrieval across hundreds of thousands of textual tokens.

## 🌐 Dashboard Portals
The application is deployed as a dual-interface research platform:
- **[Library Dashboard](http://localhost:5173)**: Focused on corpus management, file metadata, and question extraction.
- **[Alchemy Portal](http://localhost:5173#alchemy)**: A specialized hermetic blueprint interface for deep data mining, experiment extraction, and poetry analysis.

## 📈 System Maturity (V3 Hardening)
- **Reactive Event Bus**: Real-time dashboard updates via WebSockets.
- **CI/CD Pipeline**: Automated smoke tests and benchmarking for search latency.
- **Audit Stability**: 100% reversible operations via the Audit & Rollback module.

---
*Created as a capstone exploration in Data Engineering and AI-assisted knowledge management.*
