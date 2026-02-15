import sqlite3
import json
import os
import uuid
import re
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, validator

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

# --- 1. Pydantic Contracts (Validation Contracts) ---

class LawrenceOutput(BaseModel):
    """Output from Lawrence (Chymistry Analyst)"""
    allegory_term: str
    chemical_analog: str
    material_phase: str
    evidence_snippet: str
    confidence: float = Field(..., ge=0, le=1)
    historiography_tags: Dict[str, float]

class PamelaOutput(BaseModel):
    """Output from Pamela (Artisanal Tracker)"""
    artisanal_context: str
    tool: str
    practice: str
    labor_markers: List[str]
    evidence_snippet: str
    confidence: float = Field(..., ge=0, le=1)
    historiography_tags: Dict[str, float]

class WorkflowState(BaseModel):
    chunk_id: int
    text: str
    extracted_entities: List[Dict] = []
    relationships: List[Dict] = []
    historiography_scores: Dict[str, float] = {}
    run_id: int

# --- 2. Designer nodes (Logic Implementation) ---

class LawrenceNode:
    """Detects Allegories and maps to Chemical Analogs"""
    def process(self, state: WorkflowState) -> Optional[LawrenceOutput]:
        text = state.text
        # Heuristic: Look for common Allegories (Dragon, Lion, Raven)
        # and checking for chemical context (reagents, fire, vessels)
        allegories = {
            "Green Lion": "Vitriol (Iron Sulfate)",
            "Red Dragon": "Antimony or Lead state",
            "White Raven": "Sublimated Salt",
            "Philosopher's Stone": "Tincture / Universal Reagent"
        }
        
        for term, analog in allegories.items():
            if term.lower() in text.lower():
                # Extract snippet
                start = text.lower().find(term.lower())
                snippet = text[max(0, start-40):min(len(text), start+len(term)+40)]
                
                # Check for principle_empirical markers (measurements, weights)
                empirical_score = 0.4
                if re.search(r'\d+\s*(oz|drachm|ounce|part)', text): empirical_score += 0.4
                
                return LawrenceOutput(
                    allegory_term=term,
                    chemical_analog=analog,
                    material_phase="Calculated from context",
                    evidence_snippet=f"...{snippet}...",
                    confidence=0.85,
                    historiography_tags={
                        "principe_empirical": empirical_score,
                        "traditional_hermetic": 0.2 if empirical_score > 0.5 else 0.8
                    }
                )
        return None

class PamelaNode:
    """Detects Artisanal contexts and Labor verbs"""
    def process(self, state: WorkflowState) -> Optional[PamelaOutput]:
        text = state.text
        # Artisanal markers
        labor_verbs = ["grind", "seal", "stipple", "forge", "smelt", "distill", "filter", "calcine"]
        found_verbs = [v for v in labor_verbs if v in text.lower()]
        
        if found_verbs:
            # Look for equipment
            tools = ["alembic", "crucible", "furnace", "bellows", "mortar", "pestle"]
            found_tools = [t for t in tools if t in text.lower()]
            tool = found_tools[0] if found_tools else "Unknown Apparatus"
            
            # Extract snippet
            start = text.lower().find(found_verbs[0])
            snippet = text[max(0, start-40):min(len(text), start+len(found_verbs[0])+40)]
            
            return PamelaOutput(
                artisanal_context="Manual Laboratory Practice",
                tool=tool,
                practice=f"Involves {', '.join(found_verbs)}",
                labor_markers=found_verbs,
                evidence_snippet=f"...{snippet}...",
                confidence=0.75,
                historiography_tags={
                    "smith_artisanal": 0.9 if len(found_verbs) > 2 else 0.6
                }
            )
        return None

class HistoriographyScorerNode:
    """Assigns scores for principe_empirical, smith_artisanal, and traditional_hermetic"""
    def process(self, entities: List[Dict], text: str) -> Dict[str, float]:
        scores = {"principe_empirical": 0.0, "smith_artisanal": 0.0, "traditional_hermetic": 0.0}
        
        # principe_empirical markers
        if re.search(r'\d+\s*(oz|drachm|ounce|part)', text): scores["principe_empirical"] += 0.3
        if any(word in text.lower() for word in ["take", "dissolve", "mix", "heat"]): scores["principe_empirical"] += 0.3
        
        # smith_artisanal markers
        if any(word in text.lower() for word in ["grind", "seal", "forge", "smelt", "manual"]): scores["smith_artisanal"] += 0.4
        if any(word in text.lower() for word in ["guild", "workshop", "artisanal"]): scores["smith_artisanal"] += 0.3
        
        # traditional_hermetic markers
        if any(word in text.lower() for word in ["dragon", "lion", "mercury", "sulphur", "sun", "moon"]):
            if scores["principe_empirical"] < 0.3:
                scores["traditional_hermetic"] += 0.5
        
        return scores

# --- 3. Orchestrator ---

class AgenticPipeline:
    def __init__(self, run_id: int):
        self.run_id = run_id
        self.lawrence = LawrenceNode()
        self.pamela = PamelaNode()
        self.scorer = HistoriographyScorerNode()
        self.conn = sqlite3.connect(DB_PATH)

    def process_chunk(self, chunk_id: int, text: str):
        state = WorkflowState(chunk_id=chunk_id, text=text, run_id=self.run_id)
        
        # 1. Lawrence Node
        l_out = self.lawrence.process(state)
        if l_out:
            self._persist_lawrence(state, l_out)
            
        # 2. Pamela Node
        p_out = self.pamela.process(state)
        if p_out:
            self._persist_pamela(state, p_out)
            
        # 3. Global Historiography Scoring
        # In a real graph, this would aggregate all nodes' findings
        global_scores = self.scorer.process([], text)
        # Update run or chunk metadata (Optional: here we just log for now)
        # We could update the entities created in this chunk with these global scores.

    def _persist_lawrence(self, state, output: LawrenceOutput):
        cursor = self.conn.cursor()
        # Merge node scores with global scores
        final_tags = output.historiography_tags
        
        # Create Entity if not exists
        entity_id = f"allegory_{output.allegory_term.lower().replace(' ', '_')}"
        cursor.execute("INSERT OR IGNORE INTO alchemy_entities (id, category, canonical_name, normalized_name, historiography_tags, confidence, run_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (entity_id, "K: ALLEGORIES", output.allegory_term, output.allegory_term.lower(), json.dumps(final_tags), output.confidence, self.run_id))
        
        # Create Mention
        cursor.execute("INSERT INTO alchemy_mentions (entity_id, chunk_id, context_snippet, confidence, method, run_id) VALUES (?, ?, ?, ?, ?, ?)",
                       (entity_id, state.chunk_id, output.evidence_snippet, output.confidence, "lawrence_agent", self.run_id))
        
        # Relationship: analog_of
        analog_id = f"material_{output.chemical_analog.lower().replace(' ', '_')}"
        cursor.execute("INSERT OR IGNORE INTO alchemy_entities (id, category, canonical_name, normalized_name, run_id) VALUES (?, ?, ?, ?, ?)",
                       (analog_id, "MATERIALS", output.chemical_analog, output.chemical_analog.lower(), self.run_id))
        
        cursor.execute("INSERT INTO alchemy_relationships (subject_entity_id, predicate, object_entity_id, confidence, run_id) VALUES (?, ?, ?, ?, ?)",
                       (entity_id, "analog_of", analog_id, output.confidence, self.run_id))
        self.conn.commit()

    def _persist_pamela(self, state, output: PamelaOutput):
        cursor = self.conn.cursor()
        # Create Context Entity
        context_id = f"artisanal_{output.artisanal_context.lower().replace(' ', '_')}"
        cursor.execute("INSERT OR IGNORE INTO alchemy_entities (id, category, canonical_name, normalized_name, historiography_tags, confidence, run_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (context_id, "M: ARTISANAL", output.artisanal_context, output.artisanal_context.lower(), json.dumps(output.historiography_tags), output.confidence, self.run_id))
        
        # Mention
        cursor.execute("INSERT INTO alchemy_mentions (entity_id, chunk_id, context_snippet, confidence, method, run_id) VALUES (?, ?, ?, ?, ?, ?)",
                       (context_id, state.chunk_id, output.evidence_snippet, output.confidence, "pamela_agent", self.run_id))
        
        # Relationship
        tool_id = f"tool_{output.tool.lower()}"
        cursor.execute("INSERT OR IGNORE INTO alchemy_entities (id, category, canonical_name, normalized_name, run_id) VALUES (?, ?, ?, ?, ?)",
                       (tool_id, "L: TOOLS", output.tool, output.tool.lower(), self.run_id))
        
        cursor.execute("INSERT INTO alchemy_relationships (subject_entity_id, predicate, object_entity_id, confidence, run_id) VALUES (?, ?, ?, ?, ?)",
                       (context_id, "performed_with", tool_id, output.confidence, self.run_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    # Test script
    conn = sqlite3.connect(DB_PATH)
    # Register run
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alchemy_runs (notes) VALUES ('Agentic Pipeline Test Run')")
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()

    pipeline = AgenticPipeline(run_id)
    # Mock some chunks
    test_chunks = [
        (1, "Take the Green Lion and dissolve it in the acid until it becomes a salt of 2 ounces."),
        (2, "Grind the materials carefully in the mortar before you smelth them into the forge.")
    ]
    for cid, text in test_chunks:
        pipeline.process_chunk(cid, text)
    
    pipeline.close()
    print(f"Agentic Pipeline Test Run {run_id} complete.")
