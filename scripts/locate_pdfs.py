import sqlite3
import os

DB_PATH = "library.db"

def find_pdfs():
    if not os.path.exists(DB_PATH):
        print("No library.db found.")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        
        # Check for 'file_manifest' (V2 Standard)
        try:
            files = cursor.execute("SELECT current_path FROM file_manifest WHERE current_path LIKE '%.pdf' LIMIT 10").fetchall()
            if files:
                print(f"Found {len(files)} PDFs in 'file_manifest'")
                return [f[0] for f in files]
        except sqlite3.OperationalError:
            pass

        # Check for 'titles' (Legacy V1)
        try:
            files = cursor.execute("SELECT path FROM titles WHERE path LIKE '%.pdf' LIMIT 10").fetchall()
            if files:
                print(f"Found {len(files)} PDFs in 'titles'")
                return [f[0] for f in files]
        except sqlite3.OperationalError:
            pass
            
        print("No PDFs found in standard tables.")
        return []

    except Exception as e:
        print(f"Error reading DB: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    find_pdfs()
