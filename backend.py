from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
from typing import List, Optional

class MediaAssociation(BaseModel):
    title_id: int
    media_path: str
    media_type: str = "image"

app = FastAPI()

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
    query = """
        SELECT t.id, t.name, t.path, c.name, c.type, c.is_esoteric, t.summary 
        FROM titles t
        JOIN categories c ON t.category_id = c.id
        WHERE 1=1
    """
    params = []
    if category_id:
        query += " AND t.category_id = ?"
        params.append(category_id)
    if search:
        query += " AND (t.name LIKE ? OR t.summary LIKE ?)"
        params.append(f"%{search}%")
        params.append(f"%{search}%")
    if esoteric_only is not None:
        query += " AND c.is_esoteric = ?"
        params.append(esoteric_only)
        
    titles = conn.execute(query, params).fetchall()
    conn.close()
    return [{
        "id": t[0], "title": t[1], "path": t[2], "category_name": t[3], 
        "category_type": t[4], "is_esoteric": t[5], "summary": t[6]
    } for t in titles]

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
        "scholar_count": conn.execute("SELECT count(*) FROM knowledge_nodes WHERE type='scholar'").fetchone()[0],
        "message_count": conn.execute("SELECT count(*) FROM chat_messages").fetchone()[0]
    }
    conn.close()
    return stats

@app.get("/api/knowledge/scholars")
async def get_knowledge_scholars():
    conn = get_db_connection()
    scholars = conn.execute("SELECT id, name FROM knowledge_nodes WHERE type='scholar' ORDER BY name").fetchall()
    conn.close()
    return [{"id": s[0], "name": s[1]} for s in scholars]

@app.get("/api/knowledge/chats")
async def get_chats(scholar_id: Optional[int] = None):
    conn = get_db_connection()
    if scholar_id:
        chats = conn.execute("""
            SELECT c.id, c.title, c.date_created, c.model, c.msg_count 
            FROM chats c
            JOIN chat_node_links l ON c.id = l.chat_id
            WHERE l.node_id = ?
            ORDER BY c.date_created DESC
        """, (scholar_id,)).fetchall()
    else:
        chats = conn.execute("SELECT id, title, date_created, model, msg_count FROM chats ORDER BY date_created DESC").fetchall()
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
        SELECT n.name FROM knowledge_nodes n
        JOIN chat_node_links l ON n.id = l.node_id
        WHERE l.chat_id = ? AND n.type = 'scholar'
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

    # 2. Top scholars/nodes by chat association
    top_scholars = conn.execute("""
        SELECT n.name, count(l.chat_id) as chat_assoc
        FROM knowledge_nodes n
        JOIN chat_node_links l ON n.id = l.node_id
        GROUP BY n.id
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

# --- Static Files (Dashboard) ---
dist_path = os.path.join(os.path.dirname(__file__), "dashboard", "dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
