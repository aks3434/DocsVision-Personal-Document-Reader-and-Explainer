import streamlit as st
import tempfile
from pathlib import Path

from docsvision.vision.pipeline import process_document
from docsvision.document_model import build_document_model
from docsvision.scripts.query import (
    init_rag_runtime,
    answer_query_from_ui,
    ingest_doc_model_into_vectordb,
)

#-------------- Session State ----------------
if "doc_model" not in st.session_state:
    st.session_state.doc_model = None

if "ocr_result" not in st.session_state:
    st.session_state.ocr_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "doc_ingested" not in st.session_state:
    st.session_state.doc_ingested = False

if "rag_runtime" not in st.session_state:
    st.session_state.rag_runtime = None


# ---------------- Page Config ----------------
st.set_page_config(page_title="DocsVision AI", layout="wide")
st.title("📄 DocsVision AI")
st.caption("Personal Document Reader & Explainer")

# ---------------- Init RAG Runtime (ONCE) ----------------
if st.session_state.rag_runtime is None:
    with st.spinner("Initializing DocsVision (one-time setup)..."):
        st.session_state.rag_runtime = init_rag_runtime()

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader(
        "Upload PDF or Image",
        type=["pdf", "png", "jpg", "jpeg"]
    )

import hashlib

def file_hash(uploaded_file):
    return hashlib.md5(uploaded_file.getvalue()).hexdigest()

if uploaded_file is not None:
    new_hash = file_hash(uploaded_file)

    if st.session_state.get("file_hash") != new_hash:
        st.session_state.file_hash = new_hash
        st.session_state.doc_ingested = False
        st.session_state.doc_model = None     
        st.session_state.ocr_result = None     

        # 🔥 clear vector DB for new document
        vectordb = st.session_state.rag_runtime["vectordb"]
        existing = vectordb.get()
        if existing and existing.get("ids"):
            vectordb.delete(ids=existing["ids"])


# ---------------- Document Processing ----------------
if uploaded_file and st.session_state.doc_model is None:
    suffix = Path(uploaded_file.name).suffix

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        file_path = Path(tmp.name)

    with st.spinner("Running OCR & layout analysis..."):
        ocr_result = process_document(file_path)
        doc_model = build_document_model(ocr_result)

    st.session_state.ocr_result = ocr_result
    st.session_state.doc_model = doc_model
    st.session_state.doc_ingested = False

    st.sidebar.success("Document processed successfully ✅")

# ---------------- Safe Ingestion (ONCE) ----------------

if (
    st.session_state.doc_model is not None
    and st.session_state.rag_runtime is not None
    and not st.session_state.doc_ingested
):
    with st.spinner("Indexing document for search..."):
        ingest_doc_model_into_vectordb(
            st.session_state.doc_model,
            st.session_state.rag_runtime["vectordb"]
        )
    st.session_state.doc_ingested = True

doc_model = st.session_state.doc_model

# ---------------- Document Overview ----------------
if doc_model:
    st.subheader("📑 Document Overview")

    col1, col2 = st.columns(2)
    col1.metric("Pages", len(doc_model.get("pages", [])))
    col2.metric("Blocks", len(doc_model.get("blocks", [])))

# ---------------- Text Preview ----------------
if doc_model:
    with st.expander("🔍 Extracted Text (Preview)"):
        preview_text = "\n\n".join(
            block for block in doc_model.get("blocks", [])[:20] if block.strip()
        )
        st.text_area("Preview", preview_text, height=300)

# ---------------- Chat ----------------
st.markdown("---")
st.subheader("💬 Ask DocsVision")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input("Ask a question about the document...")

if user_question:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })

    answer = answer_query_from_ui(
        user_question,
        st.session_state.rag_runtime
    )

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
