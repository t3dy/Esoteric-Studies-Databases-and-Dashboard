import os
import re
import csv
import hashlib
import argparse
from audit import log_operation, mark_complete

PDF_DIR = "e:\\pdf"

def get_file_hash(path):
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def sanitize_v2(filename):
    # Remove () content
    name = re.sub(r'\(.*?\)', '', filename)
    # Preserve hyphens and underscores, remove other punctuation
    # But keep the extension dot
    ext = os.path.splitext(name)[1]
    base = os.path.splitext(name)[0]
    
    # Remove special chars but keep hyphens and underscores
    clean_base = re.sub(r'[^\w\s\-_]', '', base)
    # Collapse multiple spaces
    clean_base = re.sub(r'\s+', ' ', clean_base).strip()
    
    return clean_base + ext

def generate_plan():
    plan = []
    for root, dirs, files in os.walk(PDF_DIR):
        for f in files:
            if f.lower().endswith('.pdf'):
                old_path = os.path.join(root, f)
                new_name = sanitize_v2(f)
                new_path = os.path.join(root, new_name)
                
                if f != new_name:
                    plan.append({
                        "original": f,
                        "new": new_name,
                        "root": root,
                        "old_path": old_path,
                        "new_path": new_path
                    })
    return plan

def execute_plan(plan):
    print(f"Executing plan for {len(plan)} files...")
    success_count = 0
    for item in plan:
        try:
            # Handle collision
            final_new_path = item['new_path']
            counter = 1
            while os.path.exists(final_new_path) and final_new_path != item['old_path']:
                base, ext = os.path.splitext(item['new_path'])
                final_new_path = f"{base}_{counter}{ext}"
                counter += 1

            # Log to Audit DB
            op_id = log_operation(
                "RENAME", 
                item['old_path'], 
                {"path": item['old_path'], "name": item['original']}, 
                {"path": final_new_path, "name": os.path.basename(final_new_path)}
            )

            # Perform Rename
            os.rename(item['old_path'], final_new_path)
            
            # Mark as complete
            mark_complete(op_id)
            success_count += 1
            print(f"Renamed: {item['original']} -> {os.path.basename(final_new_path)}")
        except Exception as e:
            print(f"Error renaming {item['original']}: {e}")
            
    print(f"Successfully processed {success_count} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="V2 Ingestion & Renaming Engine")
    parser.add_argument("--apply", action="store_true", help="Apply the renames")
    parser.add_argument("--preview", action="store_true", help="Generate a preview.csv")
    args = parser.parse_args()

    plan = generate_plan()
    
    if args.preview:
        with open("rename_preview_v2.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["original", "new", "root"])
            writer.writeheader()
            for item in plan:
                writer.writerow({k: item[k] for k in ["original", "new", "root"]})
        print(f"Preview generated: rename_preview_v2.csv ({len(plan)} changes)")

    if args.apply:
        execute_plan(plan)
    elif not args.preview:
        print(f"Total potential changes: {len(plan)}. Use --preview to see them or --apply to execute.")
