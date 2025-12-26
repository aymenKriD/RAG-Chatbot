import streamlit as st
from backend.rag_backend import answer_question


# =============================
# Page Setup
# =============================
st.set_page_config(
    page_title="Call Center Knowledge Assistant",
    layout="wide"
)

# =============================
# Session State Initialization
# =============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_docs" not in st.session_state:
    st.session_state.last_docs = []


# =============================
# Sidebar: Evidence Log
# =============================
with st.sidebar:
    st.title("📚 Evidence Log")
    st.write("Conversation excerpts used for the current answer:")

    if st.session_state.last_docs:
        for i, doc in enumerate(st.session_state.last_docs, 1):
            source = doc.metadata.get("source", "Unknown")

            with st.expander(f"Document {i}: {source}"):
                st.markdown(doc.page_content[:500])
    else:
        st.info("No conversation excerpts were used for the current answer.")

    if st.button("Clear History"):
        st.session_state.messages = []
        st.session_state.last_docs = []
        st.rerun()

# =============================
# Main Chat Interface
# =============================
st.title(" Call Center Knowledge Assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =============================
# Chat Input
# =============================
if prompt := st.chat_input("Ask a question about the conversations..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching conversation history..."):
            output = answer_question(prompt)
            answer = output["answer"]
            context_docs = output["sources"]


            if context_docs:
                st.session_state.last_docs = context_docs
            else:
                st.session_state.last_docs = []

            st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            st.rerun()
