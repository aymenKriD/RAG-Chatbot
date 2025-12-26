from sqlalchemy import text
from backend.db import engine

def setup():
    with engine.connect() as conn:
        print("🛠️ Enabling pgvector extension...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        print("🛠️ Creating documents table...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding VECTOR(384),
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()
        print("✅ Database is ready!")

if __name__ == "__main__":
    setup()