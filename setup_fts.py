import sqlite3

DB_PATH = "library.db"

def setup_fts5():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create FTS5 for Chats
    print("Setting up FTS5 for Chat messages...")
    cursor.execute("DROP TABLE IF EXISTS chats_fts")
    cursor.execute("""
    CREATE VIRTUAL TABLE chats_fts USING fts5(
        chat_id UNINDEXED,
        title,
        content
    )""")

    # Populate Chats FTS
    cursor.execute("""
    INSERT INTO chats_fts (chat_id, title, content)
    SELECT c.id, c.title, m.content
    FROM chats c
    JOIN chat_messages m ON c.id = m.chat_id
    """)

    # 2. Create FTS5 for Volumes
    print("Setting up FTS5 for Volume summaries...")
    cursor.execute("DROP TABLE IF EXISTS volumes_fts")
    cursor.execute("""
    CREATE VIRTUAL TABLE volumes_fts USING fts5(
        volume_id UNINDEXED,
        title,
        summary
    )""")

    # Populate Volumes FTS
    cursor.execute("""
    INSERT INTO volumes_fts (volume_id, title, summary)
    SELECT id, title, IFNULL(summary, '') FROM titles
    """)

    conn.commit()
    conn.close()
    print("FTS5 indexing complete.")

if __name__ == "__main__":
    setup_fts5()
