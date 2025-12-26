from sentence_transformers import SentenceTransformer

# We use all-MiniLM-L6-v2: 384 dimensions, fast, and great for sentence similarity.
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    """
    Explicitly converts a string into a list of floats (vector).
    """
    # Clean the text a bit
    processed_text = text.replace("\n", " ")
    embedding = model.encode(processed_text)
    return embedding.tolist()