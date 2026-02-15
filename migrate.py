import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")
MIGRATIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_version_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version_number INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            git_commit TEXT
        )
    """)
    conn.commit()

def get_applied_versions(conn):
    cursor = conn.execute("SELECT version_number FROM schema_version ORDER BY version_number")
    return [row[0] for row in cursor.fetchall()]

def run_migrations():
    if not os.path.exists(MIGRATIONS_DIR):
        print(f"Migrations directory not found: {MIGRATIONS_DIR}")
        return

    conn = get_connection()
    init_version_table(conn)
    applied = get_applied_versions(conn)

    migration_files = sorted([f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql")])

    for filename in migration_files:
        try:
            version = int(filename.split("_")[0])
        except ValueError:
            print(f"Skipping invalid migration filename: {filename}")
            continue

        if version in applied:
            print(f"Migration {version} already applied.")
            continue

        print(f"Applying migration {version}: {filename}...")
        path = os.path.join(MIGRATIONS_DIR, filename)
        with open(path, "r") as f:
            sql = f.read()

        try:
            conn.executescript(sql)
            conn.commit()
            print(f"Migration {version} applied successfully.")
        except sqlite3.Error as e:
            conn.rollback()
            print(f"CRITICAL: Failed to apply migration {version}: {e}")
            sys.exit(1)

    # Patch for column addition (if not present)
    try:
        conn.execute("ALTER TABLE alchemy_chunks ADD COLUMN extraction_version TEXT DEFAULT '1.0'")
        conn.commit()
        print("Patched alchemy_chunks with extraction_version.")
    except sqlite3.OperationalError:
        pass # Already exists

    conn.close()

if __name__ == "__main__":
    run_migrations()
