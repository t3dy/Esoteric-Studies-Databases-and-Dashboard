import re
import os

input_file = r"C:\Users\PC\.gemini\antigravity\brain\36954c62-9d67-4848-94a4-278b6cac4051\all_files.txt"
output_file = r"C:\Users\PC\.gemini\antigravity\brain\36954c62-9d67-4848-94a4-278b6cac4051\rename_report.md"

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

report_lines = ["# Full Rename Report\n", "| ORIGINAL PATH | NEW FILENAME | STATUS |\n", "|:---|:---|:---|\n"]
for full_path in lines:
    full_path = full_path.strip()
    if not full_path: continue
    
    dir_path, name = os.path.split(full_path)
    new_name = clean_filename(name)
    
    if name != new_name:
        report_lines.append(f"| `{full_path}` | `{new_name}` | MODIFIED |\n")
    # No need to list files that don't change to keep report manageable

with open(output_file, 'w', encoding='utf8') as f:
    f.writelines(report_lines)

print(f"Report generated at {output_file}")
