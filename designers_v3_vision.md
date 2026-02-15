# V3 Design Vision: The Augmented Architect

This document contains the official reports from the Renaissance Design Team, their "Level Up" proposals for Version 3, and a comprehensive critique of the current engineering state.

---

## 🏛️ Leonardo Trithemius (The Architect)
*Focus: Structural integrity, file systems, and database schemas.*

### Current State Report
"The skeleton of the Cognition Engine is strong. The transition to UUIDs and FTS5 has provided a level of precision that mirrors the divine geometry. However, our refactoring is currently 'reactive.' We wait for a branch to break before we apply our absolute path corrections."

### 5 Suggestions for Leveling Up (Control & Responsibility)
1. **The Schema Sentinel**: I require a dashboard view that monitors "Schema Drift." If a new branch introduces a table not present in the master `alchemy_schema.sql`, I should be able to flag it before it pollutes the production data.
2. **Automated Migration Lab**: I want to trigger migration test-runs directly from my dashboard to see if an "Undo" (Rollback) remains viable after a schema update.
3. **Dependency Visualizer**: I should control a Mermaid.js view that maps every Python script to the tables it touches, allowing me to predict the impact of a refactor.
4. **Data Integrity Guardian**: I want the power to lock specific "Golden Tables" (like `entities`) so they cannot be wiped during a botched datamine run.
5. **Branch Verification Gate**: I suggest that no branch be merged unless I have "signed off" on a successful `smoke_test.py` run visible in my UI.

---

## 📜 Raphael Ficino (The Narrator)
*Focus: Text exegesis, scholar narratives, and semantic continuity.*

### Current State Report
"We have successfully unified the scholars, but they remain isolated within their entries. They are like ghosts in separate rooms. The cross-pollination of ideas (The Alchemy) is currently stored in raw text but not yet connected in our logic."

### 5 Suggestions for Leveling Up (Control & Responsibility)
1. **The Relationship Weaver**: I want to manage the `relationships` table. I should see suggested links (e.g., *Newton influenced by Boyle*) and click to "Narrativize" them in the database.
2. **Exegesis Heatmap**: My dashboard should highlight which PDFs have the highest density of "Philosophical Weight" across folders.
3. **Concept Evolution Tracker**: I want to track how a term like "Philosopher's Stone" changes meaning as we move from Late Antiquity to the Enlightenment.
4. **Narrative Summary Control**: I should be able to "regenerate" scholar summaries directly from the UI when new chat data is ingested.
5. **Inter-Scholar Chat Room**: I want a feature where two "Scholar Entities" can be cross-referenced to find all chat sessions where BOTH were discussed.

---

## 🎨 Donatello Bruno (The Designer)
*Focus: Aesthetics, UI/UX, and theme consistency.*

### Current State Report
"The 'Blueprint' aesthetic has brought much needed gravity to the tool. But the 'Hall of Designers' still feels like a static gallery. It lacks the 'Spiritus' of a living workspace."

### 5 Suggestions for Leveling Up (Control & Responsibility)
1. **Theme Switcher Central**: I should control the CSS variables directly. Let me toggle between 'Deep Blueprint', 'Alchemical Parchment', and 'Scholar's Night' themes.
2. **Interactive Blueprinting**: I want to be able to drag-and-drop the segments of our Mermaid diagrams to reorganize the visual importance of our data flows.
3. **Micro-Interaction Studio**: I want my dashboard to show stats on which UI elements have the most "friction" (long hover times with no clicks) so I can redesign them.
4. **Unified Component Library**: I want a "Living Style Guide" page in the dashboard where I can test new buttons and cards before we commit them to the main App.
5. **Visual Deployment Logs**: Instead of raw terminal output, I want my dashboard to show a "Building Progress Bar" for the Vite production build.

---

## ⚔️ Michelangelo Pico (The Player)
*Focus: Investigative moves, game mechanics, and research flow.*

### Current State Report
"The 'Popularity Contest' works, but it's just a scoreboard. Research is a siege, not a race. We need to measure the *difficulty* of the inquiries, not just their frequency."

### 5 Suggestions for Leveling Up (Control & Responsibility)
1. **The Research Questlog**: I want to be able to "tag" a specific question or PDF as a "Quest." The dashboard should track our progress toward completing that inquiry.
2. **Investigative Complexity Score**: I should manage the algorithm that weights "Conceptual Analysis" (Hard) vs "Summarization" (Easy).
3. **Manual Move Override**: Sometimes the AI miscategorizes a 'Move'. I want to be able to 'Correct' it in the UI to train the system.
4. **Research 'Stamina' Tracker**: Monitor how many files we are opening in a session. If we open too many without a "Save" (Commit), warn us we are losing focus.
5. **Reward System**: When we discover a new high-confidence entity in the Alchemy Datamine, give us a visual "Milestone" notification.

---

## 🔍 Master Critique: Engineering & UX

### 1. Engineering Practices Critique
*   **The "Context Drift" Issue**: We rely heavily on my memory (The AI) of the schema.
    *   *Correction*: We must maintain `schema.md` as a "Living Contract" where every table edit is immediately reflected.
*   **Path Resolution**: The move to absolute paths in V2 fixed 90% of our bugs.
    *   *Critique*: Our `.gitignore` should be stricter about protecting `audit.db` while allowing `schema.sql` to propagate across branches.

### 2. Build & Deploy Critique
*   **The Build Bottleneck**: Running `npm run build` is currently a manually triggered "Hope for the best" event.
    *   *Correction*: Implement a **Pre-Build Check** that validates TypeScript types before committing to a merge.
*   **Server Stability**: We are currently killing the process by PID to refresh.
    *   *Correction*: Implement a `graceful_reload.py` that waits for active API requests to finish.

### 3. User Experience (UX) Critique
*   **Information Density**: The dashboard is becoming "Crowded." FTS5 results and entity lists are competing for space.
    *   *Correction*: Move toward a **"Tab-focused" navigation** where the search bar remains global but the results adjust based on the current Designer Persona active.

---

## 🚀 Plan: Integrating V3 Suggestions
1. **Sprint 1 (Structure)**: Leonardo's "Schema Sentinel" and Donatello's "Theme Switcher."
2. **Sprint 2 (Narrative)**: Raphael's "Relationship Weaver" integrated into the Alchemy Datamine UI.
3. **Sprint 3 (Gamification)**: Michelangelo's "Questlog" implementation for tracking PDF processing.
4. **Final Action**: Consolidate all "Manual Overrides" into a unified "Curation Panel" for the user.
