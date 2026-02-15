# Plan: Esoteric Studies Knowledge System

Expand the existing PDF library into a rich knowledge database by ingesting 111+ archived chat sessions.

## Knowledge Extraction Profile

Based on analysis of the chats:
- **Table Strategy**: Often uses comparative columns (e.g., *Concept | Traditional View | Scholar View | Quote*).
- **Summarization Strategy**: Requests structured exegesis based on specific modern scholarship (Newman, Principe, Debus, Wolfson).
- **Content Types**: Tables of elements/principles, chapter summaries, and methodological analysis.

## Proposed Changes

### 1. Database Schema Update
- [NEW] `chats`: Metadata for the 111+ HTML exports.
- [NEW] `chat_content`: Full text of messages for searching.
- [NEW] `scholars`: Formal table for scholars mentioned in chats (Newman, Debus, etc.).
- [NEW] `concepts`: Key terms like "Active Intellect" or "Philosopher's Stone".
- [MODIFY] `titles`: Link titles to chats where they are discussed.

### 2. Ingestion Script (`ingest_chats.py`)
- Python script using `re` or `BeautifulSoup` to parse `index.html` files.
- Extracts Title, Date, and message pairs.
- Identifies "Keywords" (topics/scholars) to link to the main library.

### 3. Dashboard Enhancements
- **Knowledge View**: A new tab to browse by **Scholar** (linking their works and chats) or **Concept**.
- **Chat Browser**: Ability to view the archived chat logs directly in the dashboard.
- **Relational Links**: Clicking a PDF shows related chats; clicking a chat shows discussed books.

## User Review Required

> [!IMPORTANT]
> - I will parse these as regular text/HTML. Do you want me to try and reconstruct the original tables in my own database, or just link to the HTML file?
> - Should I attempt to automatically link scholars found in the chats to your subfolders (e.g., "Margaret Jacob")?

### 4. Question Analysis System
- **Extraction**: Extract individual questions (sentences ending in `?`) and critical prompts from user messages.
- **Investigative Moves**: Categorize questions like "Summarize", "Create Table", "Methodology Analysis", "Cross-Reference".
- **Database Schema**:
    - [NEW] `questions`: Stores `text`, `chat_id`, and `move_type`.

### 6. Popularity Contest
- **Aggregate Inquiry**: Calculate which topics/scholars have the most:
    - Questions asked.
    - Chat sessions associated.
    - Physical/PDF volumes in the collection.
- **Visuals**: Radar charts or comparative bar charts in a new "Inquiry Metrics" dashboard.

### 7. 'Other Topics' Portal
- **Partitioning**: Tag categories as "Esoteric" or "Other".
- **Topic Navigation**: A dedicated page for non-esoteric studies (e.g., Computer Science, Literature) with its own topic-based categorization.

## User Review Required

> [!IMPORTANT]
> - For the "Other Topics" section, how should I handle the classification? I'll start by tagging anything outside the major esoteric folders as "Other".
> - Would you like the Popularity Contest to combine data from both Esoteric and Other topics, or keep them separate?
