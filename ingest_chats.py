import os
import sqlite3
import re
from bs4 import BeautifulSoup
from datetime import datetime

DB_PATH = "library.db"
CHATS_DIR = r"e:\pdf\esoteric studies chats"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create new tables for the knowledge system
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date_created TEXT,
        date_updated TEXT,
        model TEXT,
        msg_count INTEGER,
        folder_path TEXT UNIQUE
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        role TEXT,
        content TEXT,
        FOREIGN KEY (chat_id) REFERENCES chats (id)
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        type TEXT -- scholar, concept, book, element
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_node_links (
        chat_id INTEGER,
        node_id INTEGER,
        PRIMARY KEY (chat_id, node_id),
        FOREIGN KEY (chat_id) REFERENCES chats (id),
        FOREIGN KEY (node_id) REFERENCES knowledge_nodes (id)
    )""")

    # New tables for Questions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        text TEXT,
        move_type TEXT,
        FOREIGN KEY (chat_id) REFERENCES chats (id)
    )""")
    
    conn.commit()
    return conn

def categorize_move(text):
    text = text.lower()
    if any(k in text for k in ["table", "tabular", "grid"]):
        return "Table Generation"
    if any(k in text for k in ["summarize", "summary", "overview", "briefly"]):
        return "Summarization"
    if any(k in text for k in ["methodology", "how did they", "research strategy"]):
        return "Methodology Analysis"
    if any(k in text for k in ["cite", "reference", "source", "bibliography", "scholar"]):
        return "Bibliographic Inquiry"
    if any(k in text for k in ["analyze", "discuss", "explain", "deep dive"]):
        return "Conceptual Analysis"
    return "General Question"

def extract_questions(text):
    # Strip HTML tags for clean text analysis
    clean_text = BeautifulSoup(text, "html.parser").get_text()
    # Split by common sentence ends that might hold a question
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    questions = []
    for s in sentences:
        s = s.strip()
        if s.endswith('?') or any(k in s.lower() for k in ["explain", "summarize", "show me", "create a table"]):
            if len(s) > 10: # Avoid noise
                questions.append(s)
    return questions

def parse_chat_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else os.path.basename(os.path.dirname(html_path))
    
    meta_div = soup.find('div', class_='meta')
    meta_text = meta_div.get_text() if meta_div else ""
    
    model_match = re.search(r'Model:\s*([\w\-]+)', meta_text)
    model = model_match.group(1) if model_match else ""
        
    count_match = re.search(r'(\d+)\s+messages', meta_text)
    msg_count = int(count_match.group(1)) if count_match else 0
        
    dates = re.findall(r'[A-Za-z]+\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s+[APM]{2}', meta_text)
    date_created = dates[0] if dates else ""
    date_updated = dates[1] if len(dates) > 1 else ""
    
    messages = []
    msg_divs = soup.find_all('div', class_='msg')
    for div in msg_divs:
        role_div = div.find('div', class_='role')
        bubble_div = div.find('div', class_='bubble')
        
        role = role_div.get_text().strip() if role_div else "Unknown"
        content = str(bubble_div) if bubble_div else str(div)
        messages.append((role, content))
        
    return {
        "title": title,
        "date_created": date_created,
        "date_updated": date_updated,
        "model": model,
        "msg_count": msg_count if msg_count > 0 else len(messages),
        "messages": messages
    }

def ingest_all_chats():
    conn = setup_database()
    cursor = conn.cursor()
    
    known_scholars = [
        "Newman", "Principe", "Debus", "Wolfson", "Hedesan", "Roos", 
        "Maimonides", "Abulafia", "Bruno", "Paracelsus", "Agrippa", 
        "Starkey", "Valentine", "Agricola", "Helmont", "Boyle", "Newton",
        "Hirai", "Moran", "Scholem", "Idel", "Coudert", "Clulee", "Khunrath",
        "Pico della Mirandola", "Iamblichus", "Plotinus", "Agrippa", "Trithemius", "Reuchlin"
    ]
    
    total_chats = 0
    for root, dirs, files in os.walk(CHATS_DIR):
        if "index.html" in files:
            html_path = os.path.join(root, "index.html")
            print(f"Ingesting: {html_path}")
            try:
                data = parse_chat_html(html_path)
                
                cursor.execute("""
                INSERT OR REPLACE INTO chats (title, date_created, date_updated, model, msg_count, folder_path)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (data['title'], data['date_created'], data['date_updated'], data['model'], data['msg_count'], root))
                
                cursor.execute("SELECT id FROM chats WHERE folder_path = ?", (root,))
                chat_id = cursor.fetchone()[0]
                
                cursor.execute("DELETE FROM chat_messages WHERE chat_id = ?", (chat_id,))
                cursor.execute("DELETE FROM questions WHERE chat_id = ?", (chat_id,))
                
                for role, content in data['messages']:
                    cursor.execute("INSERT INTO chat_messages (chat_id, role, content) VALUES (?, ?, ?)",
                                   (chat_id, role, content))
                    
                    if role.lower() in ["user", "you"]:
                        qs = extract_questions(content)
                        for q in qs:
                            move = categorize_move(q)
                            cursor.execute("INSERT INTO questions (chat_id, text, move_type) VALUES (?, ?, ?)",
                                           (chat_id, q, move))

                    for scholar in known_scholars:
                        if scholar.lower() in content.lower():
                            cursor.execute("INSERT OR IGNORE INTO knowledge_nodes (name, type) VALUES (?, ?)", (scholar, 'scholar'))
                            cursor.execute("SELECT id FROM knowledge_nodes WHERE name = ?", (scholar,))
                            node_id = cursor.fetchone()[0]
                            cursor.execute("INSERT OR IGNORE INTO chat_node_links (chat_id, node_id) VALUES (?, ?)", (chat_id, node_id))
                
                total_chats += 1
            except Exception as e:
                print(f"Error parsing {html_path}: {e}")
                
    conn.commit()
    print(f"Finished ingesting {total_chats} chats with question analysis.")
    conn.close()

if __name__ == "__main__":
    ingest_all_chats()
