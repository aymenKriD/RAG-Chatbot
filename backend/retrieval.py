from sqlalchemy import text
from backend.db import engine
from backend.embeddings import get_embedding

def retrieve_docs(question: str, k=3):
    """
    1. Embeds the user question.
    2. Runs a Cosine Similarity search in SQL.
    3. Returns the most relevant chunks.
    """
    # Get the vector for the question
    question_embedding = get_embedding(question)

    # SQL logic: 
    # <=> is the operator for cosine distance in pgvector.
    # We use (1 - distance) to get 'similarity'.
    query = text("""
        SELECT content, source, 1 - (embedding <=> :query_embedding) AS similarity
        FROM documents
        ORDER BY similarity DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "query_embedding": str(question_embedding),
            "limit": k
        })
        
        # Format results as a list of dictionaries
        docs = []
        for row in result:
            docs.append({
                "content": row[0],
                "source": row[1],
                "score": row[2]
            })
        return docs