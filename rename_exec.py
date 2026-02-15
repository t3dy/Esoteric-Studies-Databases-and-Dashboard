import re
import os
import shutil

input_file = r"C:\Users\PC\.gemini\antigravity\brain\36954c62-9d67-4848-94a4-278b6cac4051\all_files.txt"

def clean_filename(name):
    base, ext = os.path.splitext(name)
    # 1. Remove (...) content
    new_name = re.sub(r'\(.*?\)', '', base)
    # 2. Remove punctuation (non-alphanumeric except spaces)
    new_name = re.sub(r'[^\w\s]', ' ', new_name)
    # 3. Cleanup whitespace
    new_name = re.sub(r'\s+', ' ', new_name).strip()
    return new_name + ext

with open(input_file, 'r', encoding='utf8') as f:
    lines = f.readlines()

success_count = 0
error_count = 0
collision_count = 0

for full_path in lines:
    full_path = full_path.strip()
    if not full_path or not os.path.exists(full_path): continue
    
    dir_path, name = os.path.split(full_path)
    new_name = clean_filename(name)
    
    if name != new_name:
        new_full_path = os.path.join(dir_path, new_name)
        
        # Handle collisions
        if os.path.exists(new_full_path):
            base, ext = os.path.splitext(new_name)
            counter = 1
            while os.path.exists(os.path.join(dir_path, f"{base}_{counter}{ext}")):
                counter += 1
            new_full_path = os.path.join(dir_path, f"{base}_{counter}{ext}")
            collision_count += 1
            
        try:
            os.rename(full_path, new_full_path)
            success_count += 1
        except Exception as e:
            print(f"Error renaming {full_path}: {e}")
            error_count += 1

print(f"Renaming complete.")
print(f"Success: {success_count}")
print(f"Collisions handled: {collision_count}")
print(f"Errors: {error_count}")
