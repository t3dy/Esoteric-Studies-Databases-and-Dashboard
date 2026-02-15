import sqlite3
import os
import glob

# .../backend/app_v3/migrate.py -> Go up 3 levels to root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "library_v3.db")
MIGRATIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")

def run_migrations():
    print(f"Migrating V3 Database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    
    # Apply Genesis Migration
    sql_files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.sql")))
    
    for sql_file in sql_files:
        print(f"Applying: {os.path.basename(sql_file)}")
        with open(sql_file, "r") as f:
            sql = f.read()
            try:
                conn.executescript(sql)
                print("  -> Success")
            except Exception as e:
                print(f"  -> Failed: {e}")
                # Don't exit, genesis might be partial if re-run on existing DB without "IF NOT EXISTS"
                
    conn.close()
    print("V3 Migrations Complete.")

if __name__ == "__main__":
    run_migrations()
