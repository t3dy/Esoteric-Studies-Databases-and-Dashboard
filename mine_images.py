import sqlite3
import os
import fitz  # PyMuPDF
import hashlib
import io

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")
IMAGE_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard", "public", "assets", "extracted_images")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def mine_images():
    if not os.path.exists(IMAGE_OUTPUT_DIR):
        os.makedirs(IMAGE_OUTPUT_DIR)
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Register Run
    cursor.execute("INSERT INTO alchemy_runs (run_type, notes) VALUES (?, ?)", ("mine_images", "Extraction of images from PDF corpus"))
    run_id = cursor.lastrowid
    
    # Get all documents
    docs = cursor.execute("SELECT id, path, title FROM alchemy_documents").fetchall()
    print(f"Scanning {len(docs)} documents for images...")
    
    total_images = 0
    
    for doc in docs:
        doc_id = doc['id']
        path = doc['path']
        if not os.path.exists(path):
            continue
            
        try:
            pdf_doc = fitz.open(path)
            for page_index in range(len(pdf_doc)):
                page = pdf_doc[page_index]
                image_list = page.get_images(full=True)
                
                if image_list:
                    print(f"  - Found {len(image_list)} images in {doc['title']} p.{page_index+1}")
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    ext = base_image["ext"]
                    
                    # Generate Hash
                    image_hash = hashlib.md5(image_bytes).hexdigest()
                    
                    # Check duplication
                    exists = cursor.execute("SELECT id FROM alchemy_images WHERE image_hash = ?", (image_hash,)).fetchone()
                    if exists:
                        continue
                        
                    # Save to disk
                    filename = f"{doc_id}_{page_index+1}_{img_index}.{ext}"
                    filepath = os.path.join(IMAGE_OUTPUT_DIR, filename)
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                        
                    # Save to DB
                    # Relative path for web serving
                    web_path = f"/assets/extracted_images/{filename}"
                    
                    cursor.execute("""
                        INSERT INTO alchemy_images (document_id, page_number, image_path, image_hash, run_id, caption)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (doc_id, page_index+1, web_path, image_hash, run_id, f"Extracted from {doc['title']}"))
                    
                    total_images += 1
                    
        except Exception as e:
            print(f"Error processing {doc['title']}: {e}")
            
    conn.commit()
    conn.close()
    print(f"Image mining complete. Extracted {total_images} new images.")

if __name__ == "__main__":
    mine_images()
