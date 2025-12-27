<div align="center">
   ┌───────────────────────────┐
   │        RAG ANALYZER        │
   │   Transparent White-Box   │
   └───────────────────────────┘
Local • Explainable • SQL-Driven
</div>

---

## Overview

This project implements a **White-Box Retrieval-Augmented Generation (RAG)** system designed to analyze **call center dialogue transcripts**.

Unlike black-box solutions, every stage of the pipeline is **explicit, auditable, and locally executed**, from data ingestion to SQL-based semantic retrieval and answer generation.

The assistant answers questions **only using facts present in the transcripts**, always returning the **exact source segments** used.

---

## Key Features

- White-box RAG pipeline (fully transparent)
- Local execution (no cloud, no data leakage)
- SQL-based semantic search using `pgvector`
- Evidence-backed answers (anti-hallucination)
- Streamlit UI with source inspection

---

## Tech Stack

- **Python 3.11+**
- **PostgreSQL 16 + pgvector**
- **SQLAlchemy 2.0**
- **SentenceTransformers (MiniLM)**
- **Llama 3.1 (8B) via Ollama**
- **Streamlit**

---

## Project Structure

```plaintext
ai-expert-bot/
├── data/            # Raw call transcripts (.txt)
├── backend/         # White-box RAG logic
├── ui.py            # Streamlit interface
├── requirements.txt
└── README.md
How It Works

1-User asks a question

2-Question is embedded (384D)

3-SQL semantic search via pgvector

4-Top matching transcript chunks retrieved

5-LLM generates an answer only from retrieved sources

Example SQL retrieval:
SELECT content
FROM documents
ORDER BY embedding <=> query_vector
LIMIT 5;
##setup
python -m backend.setup_db

python -m backend.ingest_data

streamlit run ui.py
##use cases 
Call center quality audits

Agent training and coaching

Procedure and FAQ extraction

Compliance and script verification
Design Principles

Transparency over abstraction

SQL over hidden retrieval layers

Local models over cloud APIs

Evidence over speculation  
