import sqlite3
import uuid
import json

DB_PATH = "library.db"

def migrate_to_entities():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create new V2 tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entities (
        id TEXT PRIMARY KEY,
        canonical_name TEXT UNIQUE,
        normalized_name TEXT,
        category TEXT,
        metadata TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entity_mentions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_id TEXT,
        source_type TEXT,
        source_id INTEGER,
        FOREIGN KEY (entity_id) REFERENCES entities (id)
    )""")

    # Migrate from knowledge_nodes
    cursor.execute("SELECT id, name FROM knowledge_nodes")
    nodes = cursor.fetchall()
    
    print(f"Migrating {len(nodes)} nodes to entities...")
    
    for node_id, name in nodes:
        entity_id = str(uuid.uuid4())
        normalized = name.lower().strip()
        try:
            cursor.execute(
                "INSERT INTO entities (id, canonical_name, normalized_name, category) VALUES (?, ?, ?, ?)",
                (entity_id, name, normalized, 'scholar')
            )
            
            # Re-link existing chat associations
            cursor.execute("SELECT chat_id FROM chat_node_links WHERE node_id = ?", (node_id,))
            links = cursor.fetchall()
            for (chat_id,) in links:
                cursor.execute(
                    "INSERT INTO entity_mentions (entity_id, source_type, source_id) VALUES (?, ?, ?)",
                    (entity_id, 'chat', chat_id)
                )
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate: {name}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate_to_entities()
