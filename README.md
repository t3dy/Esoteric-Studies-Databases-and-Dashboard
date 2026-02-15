# 🚀 Research Cognition Engine: V3 Release
**Status:** Live (Local) | **Version:** 3.0.0 | **Commit:** `HEAD`

## 🔗 Quick Access
| Resource | URL | Version / Role |
| :--- | :--- | :--- |
| **GitHub Repository** | **[Esoteric-Studies-Databases-and-Dashboard](https://github.com/t3dy/Esoteric-Studies-Databases-and-Dashboard)** | Source Code & Version Control |
| **Documentation Hub** | **[Live Hosted Documentation](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/)** | **Start Here!** Guides & Reports |

## 🖥️ System Dashboards
*Note: The **Code** is hosted on GitHub, but the **App** requires the local Python Engine to run.*

| Version | Hosted Manual | Local App Link (Running) |
| :--- | :--- | :--- |
| **V3 (Vault)** | [Image Vault Guide](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/v3_guide.html) | [Launch Gallery](http://localhost:5173/gallery) |
| **V3 (Portal)** | [Alchemy Guide](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/v3_guide.html) | [Launch Portal](http://localhost:5173/alchemy) |
| **V2 (Graph)** | [Knowledge Graph Guide](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/v2_guide.html) | [Launch Graph](http://localhost:5173?view=knowledge) |
| **V1 (Archive)** | [Legacy Library Guide](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/v1_guide.html) | [Launch Library](http://localhost:5173?view=library) |

### 📄 Critiques & Reports
- **[Prompt Engineering Critique](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/viewer.html?doc=prompt_engineering_critique.md)**: An analysis of your feature engineering methods.
- **[Analysis Report](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/viewer.html?doc=analysis_report.md)**: System Audit.
- **[Deployment Plan](https://t3dy.github.io/Esoteric-Studies-Databases-and-Dashboard/viewer.html?doc=deployment_plan.md)**: Production Strategy.

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
