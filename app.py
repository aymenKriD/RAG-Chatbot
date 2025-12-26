import os
import pymupdf4llm

from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_postgres.vectorstores import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =============================
# Configuration
# =============================
CONNECTION_STRING = "postgresql+psycopg://postgres:23085522wqd@localhost:5432/callcenter_db"
COLLECTION_NAME = "callcenter_conversations"
MODEL_NAME = "llama3.1"
DATA_DIR = "data"

# =============================
# Helpers
# =============================
def format_docs(docs):
    """Format retrieved documents with explicit grounding."""
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        formatted.append(
            f"[Document {i} | Source: {source} | Page: {page}]\n{doc.page_content}"
        )
    return "\n\n".join(formatted)

def clean_transcript(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if ":" in line:
            speaker, content = line.split(":", 1)
            lines.append(content.strip())
    return " ".join(lines)

def validate_context(x):
    """Ensure keys always exist."""
    if not x.get("context"):
        return {"context": [], "question": x["question"]}
    return x


def refuse_if_no_context(x):
    """Hard stop if retrieval failed."""
    if not x["context"]:
        return {
            "answer": "The provided documents do not contain sufficient information to answer this question.",
            "context": []
        }
    return x


validate_context_runnable = RunnableLambda(validate_context)
refuse_if_no_context_runnable = RunnableLambda(refuse_if_no_context)

# =============================
# Initialization
# =============================
def initialize_rag():
    # Embeddings & Vector Store
    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )

    # Semantic Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )


    # =============================
    # Ingestion
    # =============================
    os.makedirs(DATA_DIR, exist_ok=True)

    for file in os.listdir(DATA_DIR):
        if not file.endswith((".txt")):
            continue

        path = os.path.join(DATA_DIR, file)

        # Prevent duplicate ingestion via metadata
        existing = vector_store.similarity_search(
            "",
            k=1,
            filter={"source": file}
        )
        if existing:
            continue

        print(f"📥 Indexing: {file}")

        with open(path, "r", encoding="latin-1") as f:
            raw_text = f.read()

        text = clean_transcript(raw_text)


        chunks = text_splitter.create_documents(
            [text],
            metadatas=[{
                "source": file,
                "domain": "CallCenter",
                "type": "conversation",
                "language": "fr"
            }]
        )

        vector_store.add_documents(chunks)

    # =============================
    # RAG Chain
    # =============================
    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 15,
        "lambda_mult": 0.6
    }
)


    llm = ChatOllama(model=MODEL_NAME)

    prompt = ChatPromptTemplate.from_template(
        """
You are a domain specialist in administrative and customer service conversations.

RULES:
- Answer ONLY using the provided conversation excerpts.
- If the answer is not explicitly stated, say:
  "The provided documents do not contain sufficient information to answer this question."
- Do NOT infer intent.
- Do NOT generalize.
- Every statement must be grounded in the documents.
- Every factual claim must reference a document number (e.g., [Document 2]).

Context:
{context}

Question:
{question}

Answer:
"""
    )

    rag_chain = (
        RunnableParallel(
            {
                "context": retriever,
                "question": RunnablePassthrough()
            }
        )
        | validate_context_runnable
        | refuse_if_no_context_runnable
    ).assign(
        answer=(
            RunnablePassthrough.assign(
                context=lambda x: format_docs(x["context"])
            )
            | prompt
            | llm
            | StrOutputParser()
        )
    )

    return rag_chain

# =============================
# CLI Test Mode
# =============================
if __name__ == "__main__":
    chain = initialize_rag()
    print("\n--- AI Specialist Bot Ready (Strict RAG Mode) ---")

    while True:
        user_input = input("\nAsk: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        result = chain.invoke(user_input)
        print("\nAssistant:")
        print(result["answer"])
