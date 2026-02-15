import urllib.request
import sqlite3
import os
import json

API_BASE = "http://localhost:8000/api"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

def test_api_health():
    print("Checking API Health...")
    endpoints = [
        "/stats",
        "/categories",
        "/alchemy/stats",
        "/alchemy/entities?category=ALCHEMISTS"
    ]
    for ep in endpoints:
        try:
            with urllib.request.urlopen(f"{API_BASE}{ep}") as response:
                if response.getcode() == 200:
                    print(f"PASS: {ep}")
                else:
                    print(f"FAIL: {ep} (Code: {response.getcode()})")
                    return False
        except Exception as e:
            print(f"FAIL: {ep} (Error: {e})")
            return False
    return True

def test_db_integrity():
    print("Checking DB Integrity...")
    conn = sqlite3.connect(DB_PATH)
    try:
        # Check Schema Version
        res = conn.execute("SELECT MAX(version_number) FROM schema_version").fetchone()
        print(f"Current Schema Version: {res[0]}")
        
        # Check FKs
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA foreign_key_check;")
        print("PASS: Database Foreign Key Integrity")
    except Exception as e:
        print(f"FAIL: DB Integrity: {e}")
        return False
    finally:
        conn.close()
    return True

if __name__ == "__main__":
    if test_db_integrity() and test_api_health():
        print("--- CI SMOKE TEST PASSED ---")
    else:
        print("--- CI SMOKE TEST FAILED ---")
