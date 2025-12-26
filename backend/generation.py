import ollama

def generate_answer(question: str, context_docs: list):
    """
    Constructs a prompt with the context and gets an answer from Llama 3.1.
    """
    
    # Format the context string
    context_text = "\n\n".join([
        f"[Source: {d['source']}] {d['content']}" 
        for d in context_docs
    ])

    prompt = f"""
You are a specialist in call center conversations.
Answer the question ONLY using the context below. 

Rules:
- If the answer isn't there, say you don't know.
- Cite your sources by filename.

Context:
{context_text}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response['message']['content']