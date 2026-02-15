import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alchemy_schema.sql")

def apply_schema():
    if not os.path.exists(SCHEMA_PATH):
        print(f"Schema file not found: {SCHEMA_PATH}")
        return

    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Applying schema to {DB_PATH}...")
    
    # Split by semicolon but be careful with triggers/etc if we had them
    # For this schema, simple split is mostly fine, or use executescript
    try:
        cursor.executescript(schema_sql)
        conn.commit()
        print("Schema applied successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        # If it's a 'no such module' error, we might be in trouble, but let's check
        if "fts5" in str(e).lower():
            print("CRITICAL: FTS5 module not found in this Python environment.")
    finally:
        conn.close()

if __name__ == "__main__":
    apply_schema()
