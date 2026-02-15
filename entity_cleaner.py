import sqlite3
import difflib

DB_PATH = "library.db"

def find_potential_merges():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, canonical_name, normalized_name FROM entities")
    entities = cursor.fetchall()
    
    merges = []
    seen = set()
    
    for i, (id1, name1, norm1) in enumerate(entities):
        if id1 in seen: continue
        for j, (id2, name2, norm2) in enumerate(entities):
            if i == j or id2 in seen: continue
            
            # Simple substring match or fuzzy ratio
            ratio = difflib.SequenceMatcher(None, norm1, norm2).ratio()
            if ratio > 0.8 or norm1 in norm2 or norm2 in norm1:
                merges.append({
                    "target": {"id": id1, "name": name1},
                    "duplicate": {"id": id2, "name": name2},
                    "score": ratio
                })
    
    conn.close()
    return merges

def apply_merge(target_id, duplicate_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Merging {duplicate_id} into {target_id}...")
    
    # 1. Re-link mentions
    cursor.execute("UPDATE entity_mentions SET entity_id = ? WHERE entity_id = ?", (target_id, duplicate_id))
    
    # 2. Delete duplicate entity
    cursor.execute("DELETE FROM entities WHERE id = ?", (duplicate_id,))
    
    conn.commit()
    conn.close()
    print("Merge complete.")

if __name__ == "__main__":
    merges = find_potential_merges()
    if not merges:
        print("No potential duplicates found.")
    else:
        print(f"Found {len(merges)} potential duplicate(s):")
        for m in merges:
            print(f"- '{m['duplicate']['name']}' might be a duplicate of '{m['target']['name']}' (Score: {m['score']:.2f})")
            # In a real tool, we'd prompt or check a config.
            # For now, let's just log them.
