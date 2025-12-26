import os
from sqlalchemy import text
from backend.db import engine
from backend.embeddings import get_embedding

DATA_DIR = "data"

def clean_transcript(text: str) -> str:
    """
    Removes speaker tags (e.g., '<01> hotesse h:') to keep only 
    the dialogue content for better embedding quality.
    """
    lines = []
    for line in text.splitlines():
        if ":" in line:
            # Split at the first colon and take the second part (the message)
            _, content = line.split(":", 1)
            lines.append(content.strip())
    return " ".join(lines)

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list:
    """
    Splits the text into overlapping chunks. 
    Overlap ensures that context isn't lost at the cut-off points.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def run_ingestion():
    if not os.path.exists(DATA_DIR):
        print(f"❌ Error: {DATA_DIR} folder not found.")
        return

    # 1. Establish connection
    with engine.connect() as conn:
        print("🧹 Cleaning old records for a fresh start...")
        conn.execute(text("TRUNCATE TABLE documents;"))
        
        # 2. Iterate through files
        for file in os.listdir(DATA_DIR):
            if file.endswith(".txt"):
                print(f"📄 Processing: {file}")
                
                path = os.path.join(DATA_DIR, file)
                try:
                    with open(path, "r", encoding="latin-1") as f:
                        raw_content = f.read()
                except Exception as e:
                    print(f"⚠️ Could not read {file}: {e}")
                    continue

                # 3. Clean and Chunk
                cleaned_text = clean_transcript(raw_content)
                chunks = chunk_text(cleaned_text)

                # 4. Embed and Store
                for chunk in chunks:
                    if not chunk.strip():
                        continue
                        
                    # Generate the vector using SentenceTransformers
                    vector = get_embedding(chunk)
                    
                    # Explicit SQL Insert
                    query = text("""
                        INSERT INTO documents (content, embedding, source)
                        VALUES (:content, :embedding, :source)
                    """)
                    
                    conn.execute(query, {
                        "content": chunk,
                        "embedding": vector,
                        "source": file
                    })
                
                # Commit after each file
                conn.commit()
                print(f"✅ Finished indexing {file}")

    print("\n🚀 Ingestion Complete! Your knowledge base is ready.")

if __name__ == "__main__":
    run_ingestion()