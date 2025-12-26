from backend.retrieval import retrieve_docs
from backend.generation import generate_answer

def answer_question(question: str) -> dict:
    # 1. Get relevant documents via SQL
    docs = retrieve_docs(question)
    
    if not docs:
        return {"answer": "No relevant documents found.", "sources": []}

    # 2. Generate answer using Llama 3.1
    answer = generate_answer(question, docs)

    # 3. Format for Streamlit (matches your UI expectations)
    # We map 'content' to 'page_content' and 'source' to 'metadata' 
    # so your existing UI code doesn't break.
    formatted_sources = []
    for d in docs:
        # Create a dummy object or dict that mimics the LangChain Doc structure your UI likes
        class Doc:
            def __init__(self, c, s):
                self.page_content = c
                self.metadata = {"source": s}
        
        formatted_sources.append(Doc(d['content'], d['source']))

    return {
        "answer": answer,
        "sources": formatted_sources
    }