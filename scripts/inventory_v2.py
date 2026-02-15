import sqlite3
import json
import os
import sys

# Add root to sys.path to import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend import app
except ImportError:
    # If running after move, try backend.app_v2.main
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "app_v2"))
    from main import app

DB_PATH = "library.db"

def dump_schema():
    if not os.path.exists(DB_PATH):
        print("No library.db found.")
        return {}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    schema = {}
    
    # Tables
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for t in tables:
        table_name = t[0]
        columns = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        schema[table_name] = [
            {"cid": c[0], "name": c[1], "type": c[2], "notnull": c[3], "pk": c[5]}
            for c in columns
        ]
    
    conn.close()
    return schema

def dump_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, "methods"):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name
            })
    return routes

if __name__ == "__main__":
    inventory = {
        "schema": dump_schema(),
        "routes": dump_routes()
    }
    
    with open("v2_inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    print("V2 Inventory dumped to v2_inventory.json")
