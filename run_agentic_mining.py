import sqlite3
import os
from agentic_pipeline import AgenticPipeline

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

def run_agentic_mining():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # 1. Register Run
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alchemy_runs (notes) VALUES ('Production Agentic Workflow Run (Lawrence & Pamela)')")
    run_id = cursor.lastrowid
    conn.commit()
    
    print(f"Starting Agentic Workflow Run ID: {run_id}")
    pipeline = AgenticPipeline(run_id)
    
    # 2. Iterate All Alchemy Chunks
    chunks = conn.execute("SELECT id, text_clean FROM alchemy_chunks").fetchall()
    print(f"Processing {len(chunks)} chunks...")
    
    for i, chunk in enumerate(chunks):
        pipeline.process_chunk(chunk['id'], chunk['text_clean'])
        if i % 100 == 0:
            print(f"  Processed {i}/{len(chunks)} chunks...")
            
    pipeline.close()
    conn.close()
    print("Agentic Mining Pipeline Complete.")

if __name__ == "__main__":
    run_agentic_mining()
