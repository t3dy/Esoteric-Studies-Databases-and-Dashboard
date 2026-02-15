import os
import shutil

INBOX = r"e:\pdf\databaseINBOX"
BASE_DIR = r"e:\pdf"

MAPPING = {
    "alchemy": os.path.join(BASE_DIR, "alchemy"),
    "kabbalah": os.path.join(BASE_DIR, "esoteric studies", "kabbalah"),
    "hermetica": os.path.join(BASE_DIR, "esoteric studies", "hermetica"),
    "occult": os.path.join(BASE_DIR, "esoteric studies", "occult"),
    "philosophy": os.path.join(BASE_DIR, "esoteric studies", "philosophy"),
    "lit": os.path.join(BASE_DIR, "other topics", "lit"),
    "tmnt": os.path.join(BASE_DIR, "comics", "tmnt"),
    "marvel_dc": os.path.join(BASE_DIR, "comics", "marvel_dc")
}

def route_files():
    if not os.path.exists(INBOX):
        print("Inbox not found.")
        return

    for filename in os.listdir(INBOX):
        lowered = filename.lower()
        target = None
        
        # Heuristics
        if "tmnt" in lowered or "teenage mutant ninja turtles" in lowered:
            target = MAPPING["tmnt"]
        elif "batman" in lowered or "spider-man" in lowered or "marvel" in lowered:
            target = MAPPING["marvel_dc"]
        elif "alchem" in lowered or "chemistry" in lowered or "debus" in lowered or "obrist" in lowered:
            target = MAPPING["alchemy"]
        elif "yetzirah" in lowered or "kabbalah" in lowered or "akiba" in lowered or "saadia" in lowered:
            target = MAPPING["kabbalah"]
        elif "hermet" in lowered or "poimandres" in lowered or "zosimos" in lowered:
            target = MAPPING["hermetica"]
        elif "agrippa" in lowered or "pico" in lowered or "ars notoria" in lowered or "occult" in lowered:
            target = MAPPING["occult"]
        elif "swedenborg" in lowered or "hadot" in lowered:
            target = MAPPING["philosophy"]
        elif "shakespeare" in lowered or "jonson" in lowered or "goethe" in lowered:
            target = MAPPING["lit"]
            
        if target:
            if not os.path.exists(target):
                os.makedirs(target)
            
            src = os.path.join(INBOX, filename)
            dst = os.path.join(target, filename)
            
            try:
                shutil.move(src, dst)
                print(f"Moved {filename} -> {target}")
            except Exception as e:
                print(f"Error moving {filename}: {e}")
        else:
            print(f"No route for {filename}")

if __name__ == "__main__":
    route_files()
