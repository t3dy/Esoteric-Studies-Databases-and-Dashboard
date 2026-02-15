import sqlite3
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIT_DB = os.path.join(BASE_DIR, "audit.db")

def init_audit_db():
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        operation TEXT,
        target_path TEXT,
        pre_state TEXT,
        post_state TEXT,
        status TEXT DEFAULT 'PENDING'
    )""")
    conn.commit()
    conn.close()

def log_operation(operation, target_path, pre_state, post_state):
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO audit_log (operation, target_path, pre_state, post_state) VALUES (?, ?, ?, ?)",
        (operation, target_path, json.dumps(pre_state), json.dumps(post_state))
    )
    op_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return op_id

def mark_complete(op_id):
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE audit_log SET status = 'COMPLETED' WHERE id = ?", (op_id,))
    conn.commit()
    conn.close()

def get_last_ops(limit=10):
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, operation, target_path, status FROM audit_log ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize on import
init_audit_db()

if __name__ == "__main__":
    print(f"Audit database initialized at: {AUDIT_DB}")
