<div align="center">
<pre>
┌───────────────────────────┐
│        RAG ANALYZER        │
│   Transparent White-Box    │
└───────────────────────────┘
</pre>
<p><strong>Local • Explainable • SQL-Driven</strong></p>
</div>

<hr>

<h2>Overview</h2>
<p>This project implements a <strong>White-Box Retrieval-Augmented Generation (RAG)</strong> system designed to analyze <strong>call center dialogue transcripts</strong>.</p>
<p>Unlike black-box solutions, every stage of the pipeline is <strong>explicit, auditable, and locally executed</strong>, from data ingestion to SQL-based semantic retrieval and answer generation.</p>
<p>The assistant answers questions <strong>strictly based on the transcripts</strong>, always returning the <strong>exact source segments</strong> used.</p>

<hr>

<h2>Key Features</h2>
<ul>
<li>Fully transparent White-box RAG pipeline</li>
<li>Local execution (no cloud, no data leakage)</li>
<li>SQL-based semantic search using <code>pgvector</code></li>
<li>Evidence-backed answers (anti-hallucination)</li>
<li>Streamlit UI with source inspection</li>
</ul>

<hr>

<h2>Tech Stack</h2>
<ul>
<li><strong>Python 3.11+</strong></li>
<li><strong>PostgreSQL 16 + pgvector</strong></li>
<li><strong>SQLAlchemy 2.0</strong></li>
<li><strong>SentenceTransformers (MiniLM)</strong></li>
<li><strong>Llama 3.1 (8B) via Ollama</strong></li>
<li><strong>Streamlit</strong></li>
</ul>

<hr>

<h2>Project Structure</h2>
<pre>
ai-expert-bot/
├── data/            # Raw call transcripts (.txt)
├── backend/         # White-box RAG logic
├── ui.py            # Streamlit interface
├── requirements.txt
└── README.md
</pre>

<hr>

<h2>How It Works</h2>
<ol>
<li><strong>User asks a question</strong></li>
<li><strong>Question is embedded</strong> into a 384-dimensional vector</li>
<li><strong>SQL semantic search</strong> via <code>pgvector</code></li>
<li><strong>Top matching transcript chunks</strong> are retrieved</li>
<li><strong>LLM gener
