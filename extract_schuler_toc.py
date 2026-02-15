import fitz
import sys

pdf_path = r"e:\pdf\alchemy\poetry lit\Alchemical Poetry 1575 1700_ From Previously Unpublished Manuscripts 5 Routledge.pdf"

def extract_toc():
    try:
        doc = fitz.open(pdf_path)
        # Usually TOC is in the first 1-15 pages
        for i in range(5, 12):
            print(f"--- Page {i} ---")
            print(doc[i].get_text())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_toc()
