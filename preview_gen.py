import re
import os

files = [
    r"Yevgeny Zamyatin - We (1987, Avon Books).pdf",
    r"(Princeton Legacy Library_ 555) Jonathan F.S. Post - Henry Vaughan_ The Unfolding Vision-Princeton University Press (2014).pdf",
    r"(History, Philosophy and Theory of the Life Sciences 2) Sebastian Normandin, Charles T. Wolfe (auth.), Sebastian Normandin, Charles T. Wolfe (eds.) - Vitalism and the Scientific Image in Post-Enlighte.pdf",
    r"R. A. Durr - On the Mystical Poetry of Henry Vaughan-Harvard University Press (1962).pdf",
    r"witchcraft studies Hutton\Ronald Hutton - Witches, Druids and King Arthur (2006, Bloomsbury Academic) - libgen.li.pdf",
    r"haunt\[Palgrave Gothic] Joakim Wrethed - Gothic Hauntology_ Everyday Hauntings and Epistemological Desire (2023, Palgrave Macmillan) - libgen.li.pdf"
]

def clean_filename(filename):
    path, name = os.path.split(filename)
    base, ext = os.path.splitext(name)
    
    # 1. Remove (...) content
    new_name = re.sub(r'\(.*?\)', '', base)
    
    # 2. Remove punctuation - interpreting "the punctuation mark" as any non-alphanumeric (except folders)
    # Actually, I'll keep spaces.
    new_name = re.sub(r'[^\w\s]', ' ', new_name)
    
    # 3. Cleanup whitespace
    new_name = re.sub(r'\s+', ' ', new_name).strip()
    
    return os.path.join(path, new_name + ext)

print("| BEFORE | AFTER |")
print("|--------|-------|")
for f in files:
    clean = clean_filename(os.path.basename(f))
    print(f"| {os.path.basename(f)} | {clean} |")
