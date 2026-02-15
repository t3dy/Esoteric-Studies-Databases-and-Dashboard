import sqlite3
import os
import re

DB_PATH = r"C:\Users\PC\.gemini\antigravity\brain\36954c62-9d67-4848-94a4-278b6cac4051\library.db"
ROOT_DIR = r"e:\pdf"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT CHECK(type IN ('scholar', 'topic', 'other')) DEFAULT 'topic'
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS titles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        path TEXT UNIQUE NOT NULL,
        category_id INTEGER,
        author TEXT,
        year TEXT,
        summary TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_id INTEGER,
        media_path TEXT NOT NULL,
        media_type TEXT,
        FOREIGN KEY (title_id) REFERENCES titles (id)
    )''')
    
    conn.commit()
    return conn

def scan_files(conn):
    cursor = conn.cursor()
    
    # Known scholars to prioritize categorization
    scholars = ["Cavendish", "Margaret Jacob", "Idriesh Shah", "Shakespeare", "Idries Shah", "albertus magnus", "Hilma af Klint", "pkd"]
    
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                
                # Determine Category based on immediate parent folder
                parent_folder = os.path.basename(root)
                if parent_folder == "pdf": # Root level
                    category_name = "Unsorted"
                else:
                    category_name = parent_folder
                
                # Determine Category Type
                cat_type = 'topic'
                if any(s.lower() in category_name.lower() for s in scholars):
                    cat_type = 'scholar'
                
                # Insert Category
                cursor.execute('INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)', (category_name, cat_type))
                cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
                category_id = cursor.fetchone()[0]
                
                # Insert Title
                title = os.path.splitext(file)[0]
                cursor.execute('''
                INSERT OR IGNORE INTO titles (title, path, category_id) 
                VALUES (?, ?, ?)
                ''', (title, full_path, category_id))
                
    conn.commit()

if __name__ == "__main__":
    print(f"Initializing database at {DB_PATH}...")
    connection = init_db()
    print("Scanning files and indexing...")
    scan_files(connection)
    
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM titles")
    count = cursor.fetchone()[0]
    print(f"Indexing complete. Total titles: {count}")
    connection.close()
