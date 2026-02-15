import os
import shutil
import sys

# Import the locator logic
try:
    from locate_pdfs import find_pdfs
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from locate_pdfs import find_pdfs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_DIR = os.path.join(BASE_DIR, "tests", "fixtures", "pdfs")

def setup_fixtures():
    print(f"Setting up fixtures in {FIXTURES_DIR}...")
    if not os.path.exists(FIXTURES_DIR):
        os.makedirs(FIXTURES_DIR)
        
    pdf_paths = find_pdfs()
    if not pdf_paths:
        print("No PDFs found in DB to use as fixtures.")
        return

    count = 0
    for path in pdf_paths:
        if os.path.exists(path):
            filename = os.path.basename(path)
            dest = os.path.join(FIXTURES_DIR, filename)
            if not os.path.exists(dest):
                shutil.copy2(path, dest)
                print(f"Copied: {filename}")
                count += 1
            else:
                print(f"Exists: {filename}")
        else:
            print(f"Missing Source File: {path}")
            
    print(f"Setup Complete. {count} new fixtures added.")

if __name__ == "__main__":
    setup_fixtures()
