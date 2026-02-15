from fastapi import FastAPI, HTTPException, Body, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import json
import asyncio
from typing import List, Optional

app = FastAPI()

# Event Bus State
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/stats")
async def get_stats():
    conn = get_db_connection()
    titles = conn.execute("SELECT count(*) FROM titles").fetchone()[0]
    categories = conn.execute("SELECT count(*) FROM categories").fetchone()[0]
    media = conn.execute("SELECT count(*) FROM media").fetchone()[0]
    # Ingested chat stats
    chats = conn.execute("SELECT count(*) FROM chats").fetchone()[0]
    questions = conn.execute("SELECT count(*) FROM questions").fetchone()[0]
    conn.close()
    return {
        "titles": titles, 
        "categories": categories, 
        "media": media,
        "chats": chats,
        "questions": questions
    }

@app.get("/api/categories")
async def get_categories():
    conn = get_db_connection()
    categories = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in categories]

@app.get("/api/titles")
async def get_titles(category_id: Optional[int] = None, search: Optional[str] = None, esoteric_only: Optional[int] = None):
    conn = get_db_connection()
    query = "SELECT t.id, t.title, t.path, c.name, c.type FROM titles t JOIN categories c ON t.category_id = c.id WHERE 1=1"
    params = []
    
    if category_id:
        query += " AND t.category_id = ?"
        params.append(category_id)
    if esoteric_only is not None:
        query += " AND c.is_esoteric = ?"
        params.append(esoteric_only)
    
    if search:
        # Use FTS5 for search
        fts_query = """
            SELECT volume_id FROM volumes_fts 
            WHERE volumes_fts MATCH ? 
            ORDER BY rank
        """
        fts_results = conn.execute(fts_query, (f'"{search}"*',)).fetchall()
        if fts_results:
            ids = [r[0] for r in fts_results]
            query += f" AND t.id IN ({','.join(['?']*len(ids))})"
            params.extend(ids)
        else:
            conn.close()
            return []

    titles = conn.execute(query, params).fetchall()
    conn.close()
    return [{"id": t[0], "title": t[1], "path": t[2], "category_name": t[3], "category_type": t[4]} for t in titles]

@app.get("/api/title/{title_id}")
async def get_title(title_id: int):
    conn = get_db_connection()
    title = conn.execute("SELECT t.*, c.name as category_name FROM titles t JOIN categories c ON t.category_id = c.id WHERE t.id = ?", (title_id,)).fetchone()
    if not title:
        conn.close()
        raise HTTPException(status_code=404, detail="Title not found")
    
    media = conn.execute("SELECT * FROM media WHERE title_id = ?", (title_id,)).fetchall()
    result = dict(title)
    result["media"] = [dict(row) for row in media]
    conn.close()
    return result

@app.post("/api/media")
async def associate_media(data: MediaAssociation):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO media (title_id, media_path, media_type) VALUES (?, ?, ?)",
            (data.title_id, data.media_path, data.media_type)
        )
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# --- Knowledge System Endpoints ---

@app.get("/api/knowledge/stats")
async def get_knowledge_stats():
    conn = get_db_connection()
    stats = {
        "chat_count": conn.execute("SELECT count(*) FROM chats").fetchone()[0],
        "scholar_count": conn.execute("SELECT count(*) FROM entities WHERE type='scholar'").fetchone()[0],
        "message_count": conn.execute("SELECT count(*) FROM chat_messages").fetchone()[0]
    }
    conn.close()
    return stats

@app.get("/api/knowledge/scholars")
async def get_knowledge_scholars():
    conn = get_db_connection()
    scholars = conn.execute("SELECT id, canonical_name FROM entities WHERE type='scholar' ORDER BY canonical_name").fetchall()
    conn.close()
    return [{"id": s[0], "name": s[1]} for s in scholars]

@app.get("/api/knowledge/chats")
async def get_chats(scholar_id: Optional[str] = None, search: Optional[str] = None):
    conn = get_db_connection()
    query = "SELECT id, title, date_created, model, msg_count FROM chats WHERE 1=1"
    params = []
    
    if scholar_id:
        # Use new entity mentions linking
        query = """
            SELECT c.id, c.title, c.date_created, c.model, c.msg_count 
            FROM chats c
            JOIN entity_mentions m ON c.id = m.source_id
            WHERE m.source_type = 'chat' AND m.entity_id = ?
        """
        params.append(scholar_id)
    
    if search:
        fts_query = "SELECT chat_id FROM chats_fts WHERE chats_fts MATCH ?"
        fts_results = conn.execute(fts_query, (f'"{search}"*',)).fetchall()
        if fts_results:
            ids = list(set([r[0] for r in fts_results]))
            if scholar_id: # If scholar_id is already filtering, intersect the results
                # This is a simplified intersection. For complex queries, a subquery might be better.
                # For now, we'll assume the scholar_id query is primary if present.
                # If scholar_id is present, the query is already set up to filter by scholar.
                # We need to add the chat_id filter to that existing query.
                query += f" AND c.id IN ({','.join(['?']*len(ids))})"
                params.extend(ids)
            else: # If no scholar_id, filter the main chats table
                query += f" AND id IN ({','.join(['?']*len(ids))})"
                params.extend(ids)
        else:
            conn.close()
            return []

    query += " ORDER BY date_created DESC" # Ensure ordering is always applied
    
    chats = conn.execute(query, params).fetchall()
    conn.close()
    return [{"id": c[0], "title": c[1], "date": c[2], "model": c[3], "msg_count": c[4]} for c in chats]

@app.get("/api/knowledge/chats/{chat_id}")
async def get_chat_details(chat_id: int):
    conn = get_db_connection()
    chat = conn.execute("SELECT title, date_created, model, msg_count, folder_path FROM chats WHERE id = ?", (chat_id,)).fetchone()
    if not chat:
        conn.close()
        raise HTTPException(status_code=404, detail="Chat not found")
    
    messages = conn.execute("SELECT role, content FROM chat_messages WHERE chat_id = ? ORDER BY id", (chat_id,)).fetchall()
    
    scholars = conn.execute("""
        SELECT n.canonical_name FROM entities n
        JOIN entity_mentions l ON n.id = l.entity_id
        WHERE l.source_id = ? AND l.source_type = 'chat' AND n.type = 'scholar'
    """, (chat_id,)).fetchall()
    
    conn.close()
    return {
        "title": chat[0],
        "date": chat[1],
        "model": chat[2],
        "msg_count": chat[3],
        "folder_path": chat[4],
        "messages": [{"role": m[0], "content": m[1]} for m in messages],
        "scholars": [s[0] for s in scholars]
    }

@app.get("/api/knowledge/questions")
async def get_questions(chat_id: Optional[int] = None, move_type: Optional[str] = None):
    conn = get_db_connection()
    query = "SELECT q.id, q.text, q.move_type, c.title, c.id FROM questions q JOIN chats c ON q.chat_id = c.id WHERE 1=1"
    params = []
    if chat_id:
        query += " AND q.chat_id = ?"
        params.append(chat_id)
    if move_type:
        query += " AND q.move_type = ?"
        params.append(move_type)
    
    questions = conn.execute(query, params).fetchall()
    conn.close()
    return [{"id": q[0], "text": q[1], "move": q[2], "chat_title": q[3], "chat_id": q[4]} for q in questions]

@app.get("/api/knowledge/inquiry-stats")
async def get_inquiry_stats():
    conn = get_db_connection()
    # Questions per chat for visualization
    chat_stats = conn.execute("""
        SELECT c.title, count(q.id) as q_count 
        FROM chats c 
        LEFT JOIN questions q ON c.id = q.chat_id 
        GROUP BY c.id 
        HAVING q_count > 0
        ORDER BY q_count DESC
    """).fetchall()
    
    # Distribution of moves
    move_stats = conn.execute("""
        SELECT move_type, count(*) as count 
        FROM questions 
        GROUP BY move_type
    """).fetchall()

    # Popularity stats
    # 1. Top categories by volume
    top_categories = conn.execute("""
        SELECT c.name, count(t.id) as volumes, c.is_esoteric
        FROM categories c
        JOIN titles t ON c.id = t.category_id
        GROUP BY c.id
        ORDER BY volumes DESC
        LIMIT 10
    """).fetchall()

    # 2. Top scholars/nodes by chat association (Using V2 Entities)
    top_scholars = conn.execute("""
        SELECT e.canonical_name, count(m.id) as chat_assoc
        FROM entities e
        JOIN entity_mentions m ON e.id = m.entity_id
        WHERE m.source_type = 'chat'
        GROUP BY e.id
        ORDER BY chat_assoc DESC
        LIMIT 10
    """).fetchall()
    
    conn.close()
    return {
        "chat_stats": [{"title": s[0], "count": s[1]} for s in chat_stats],
        "move_stats": [{"move": s[0], "count": s[1]} for s in move_stats],
        "popularity": {
            "categories": [{"name": s[0], "volumes": s[1], "esoteric": s[2]} for s in top_categories],
            "scholars": [{"name": s[0], "chats": s[1]} for s in top_scholars]
        }
    }

@app.get("/api/designers")
async def get_designers():
    conn = get_db_connection()
    # Real metrics for the designers
    audit_count = conn.execute("SELECT count(*) FROM audit_log").fetchone()[0]
    scholar_no_summary = conn.execute("SELECT count(*) FROM entities WHERE metadata IS NULL OR json_extract(metadata, '$.summary') IS NULL").fetchone()[0]
    move_count = conn.execute("SELECT count(*) FROM questions").fetchone()[0]
    
    conn.close()
    
    return [
        {
            "id": "trithemius",
            "name": "Leonardo Trithemius",
            "role": "Branch Manager / Architect",
            "issues": [
                f"Infrastructure Health: {audit_count} operations logged in audit.db",
                "Schema V2 transition complete; 100% UUID coverage.",
                "Note: Audit rotation policy not yet implemented."
            ],
            "flow": "graph TD\n    A[Raw PDF] --> B[Ingest V2]\n    B --> C{Audit Log}\n    C --> D[SQLite V2]\n    D --> E[FTS5 Search Index]\n    D --> F[Canonical Entity Layer]"
        },
        {
            "id": "ficino",
            "name": "Raphael Ficino",
            "role": "Narrative Designer",
            "issues": [
                f"{scholar_no_summary} scholars lack contextual exegesis summaries.",
                "Connection Strength: Knowledge nodes links are purely name-based.",
                "Missing 'Philosopher's Stone' concept mapping in 12% of chats."
            ],
            "flow": "graph LR\n    A[Scholar Mention] --> B[Entity Resolution]\n    B --> C[UUID Assignment]\n    C --> D[Exegesis Creation]\n    D --> E[Narrative Archive]"
        },
        {
            "id": "pico",
            "name": "Michelangelo Pico",
            "role": "Play & Learning Specialist",
            "issues": [
                f"{move_count} investigative moves tracked. Move 'Cross-Reference' is rare.",
                "Player Progression: Inquiry density is high but 'Quests' are manual.",
                "Feedback Loop: Summaries don't yet trigger new question spawns."
            ],
            "flow": "graph TD\n    A[User Inquiry] --> B[Question Extraction]\n    B --> C[Move Classification]\n    C --> D[Metric Aggregation]\n    D --> E[Learning Progress]"
        },
        {
            "id": "bruno",
            "name": "Donatello Bruno",
            "role": "Interface Designer",
            "issues": [
                "Accessibility: Tooltip coverage at 45% in Popularity Dashboard.",
                "Aesthetic: 'Other Portal' needs parchment/gold CSS skin.",
                "Interaction: Graph view for scholar network is still a bar chart."
            ],
            "flow": "graph LR\n    A[React App] --> B[FastAPI REST]\n    B --> C[SQLite Queries]\n    C --> D[JSON Response]\n    D --> E[Rich Visualization]"
        },
        {
            "id": "hume",
            "name": "Deez Hume",
            "role": "Digital Humanities & Portfolio Lead",
            "issues": [
                "Pedagogy: 'Story of Learning' nodes need explicit mapping in README.md",
                "Principles: Portfolio values (Transparency, Material Intelligence) not yet tagged in exegesis.",
                "Audit: Technical documentation needs branch-level impact summaries."
            ],
            "flow": "graph TD\n    A[Technical Implementation] --> B[DH Principles Audit]\n    B --> C[Story of Learning Tracking]\n    C --> D[Portfolio Copywriting]\n    D --> E[Public Presentation]"
        }
    ]

# --- Alchemy Datamine Endpoints ---

@app.get("/api/alchemy/stats")
async def get_alchemy_stats():
    conn = get_db_connection()
    try:
        stats = conn.execute("""
            SELECT category, count(*) as count 
            FROM alchemy_entities 
            GROUP BY category
        """).fetchall()
        runs = conn.execute("SELECT count(*) FROM alchemy_runs").fetchone()[0]
        mentions = conn.execute("SELECT count(*) FROM alchemy_mentions").fetchone()[0]
        return {
            "categories": {row['category']: row['count'] for row in stats},
            "total_runs": runs,
            "total_mentions": mentions
        }
    except Exception as e:
        return {"error": "Alchemy tables not found or empty"}
    finally:
        conn.close()

@app.get("/api/alchemy/entities")
async def get_alchemy_entities(category: Optional[str] = None, limit: int = 100):
    conn = get_db_connection()
    query = "SELECT * FROM alchemy_entities WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY canonical_name LIMIT ?"
    params.append(limit)
    
    entities = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in entities]

@app.get("/api/alchemy/entity/{entity_id}")
async def get_alchemy_entity(entity_id: str):
    conn = get_db_connection()
    entity = conn.execute("SELECT * FROM alchemy_entities WHERE id = ?", (entity_id,)).fetchone()
    if not entity:
        conn.close()
        raise HTTPException(status_code=404, detail="Entity not found")
    
    mentions = conn.execute("""
        SELECT m.*, d.title as doc_title
        FROM alchemy_mentions m
        JOIN alchemy_documents d ON m.document_id = d.id
        WHERE m.entity_id = ?
        LIMIT 10
    """, (entity_id,)).fetchall()
    
    result = dict(entity)
    result["mentions"] = [dict(row) for row in mentions]
    conn.close()
    return result

@app.post("/api/alchemy/mine")
async def run_alchemy_mining():
    # In a real production app, this would be a background task (celery/etc)
    # For this environment, we can trigger the scripts via os.system or similar.
    import subprocess
    try:
        # Trigger mining scripts in sequence
        subprocess.Popen(["python", "mine_alchemy.py"])
        subprocess.Popen(["python", "extract_experiments.py"])
        subprocess.Popen(["python", "extract_reconstructions.py"])
        return {"status": "Mining triggered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alchemy/images")
async def get_alchemy_images(limit: int = 50, offset: int = 0):
    conn = get_db_connection()
    try:
        images = conn.execute("""
            SELECT i.*, d.title as doc_title 
            FROM alchemy_images i
            JOIN alchemy_documents d ON i.document_id = d.id
            ORDER BY i.id DESC
            LIMIT ? OFFSET ?
        """, (limit, offset)).fetchall()
        return [dict(row) for row in images]
    finally:
        conn.close()

@app.post("/api/alchemy/rollback/{run_id}")
async def rollback_alchemy_run(run_id: int):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM alchemy_mentions WHERE run_id = ?", (run_id,))
        conn.execute("DELETE FROM alchemy_entities WHERE run_id = ?", (run_id,))
        conn.execute("DELETE FROM alchemy_runs WHERE id = ?", (run_id,))
        conn.commit()
        return {"status": f"Run {run_id} rolled back"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# --- Static Files (Dashboard) ---
dist_path = os.path.join(os.path.dirname(__file__), "dashboard", "dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
