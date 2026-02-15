import sqlite3
import os
import json
import shutil
from audit import AUDIT_DB

def rollback_last_op():
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, operation, target_path, pre_state, post_state FROM audit_log WHERE status = 'COMPLETED' ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
        print("No completed operations found in the audit log.")
        return

    op_id, op_type, path, pre_state_json, post_state_json = row
    pre_state = json.loads(pre_state_json)
    post_state = json.loads(post_state_json)

    print(f"Rolling back operation {op_id}: {op_type} on {path}")

    try:
        if op_type == "RENAME":
            old_path = pre_state['path']
            new_path = post_state['path']
            if os.path.exists(new_path):
                os.rename(new_path, old_path)
                print(f"Restored: {new_path} -> {old_path}")
            else:
                print(f"Error: Current path {new_path} not found.")
                return

        # Mark as ROLLBACKED
        cursor.execute("UPDATE audit_log SET status = 'ROLLBACKED' WHERE id = ?", (op_id,))
        conn.commit()
        print(f"Success: Operation {op_id} rolled back.")

    except Exception as e:
        print(f"Rollback failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    rollback_last_op()
