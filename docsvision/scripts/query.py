"""
query.py

Usage:
python scripts/query.py
"""
from docsvision.rag.intent import classify_intent
from docsvision.core.embedding import get_embeddings
from docsvision.core.vectordb import load_vectorstore
from docsvision.core.retriever import DocsVisionRetriever
from docsvision.core.llm import get_llm
from docsvision.core.llm import get_fast_llm
from docsvision.rag.chain import build_rag_chain
from streamlit import session_state


def extract_clean_text(doc_model):
    texts = []

    for block in doc_model["blocks"]:
        if isinstance(block, str):
            if block.strip():
                texts.append(block.strip())

        elif isinstance(block, dict):
            text = block.get("text", "").strip()
            if text:
                texts.append(text)

    return texts


def is_meta_document_question(question: str) -> bool:
    q = question.lower().split()

    DOCUMENT_REFERENCES = {
        "document", "file", "pdf", "assignment",
        "report", "notes", "attached", "this"
    }

    OVERVIEW_VERBS = {
        "about", "describe", "summarize", "explain",
        "overview", "tell", "what"
    }

    return (
        any(word in q for word in DOCUMENT_REFERENCES)
        and any(word in q for word in OVERVIEW_VERBS)
    )



STOPWORDS = {
    "what", "is", "the", "of", "a", "an", "to", "in", "on",
    "for", "and", "or", "about", "based", "does", "do"
}

def is_context_sufficient(docs, question: str, min_chars: int = 50) -> bool:
    if not docs:
        return False

    # ✅ META-QUESTION BYPASS
    if is_meta_document_question(question):
        return True

    # total content check
    total_text = sum(len(doc.page_content.strip()) for doc in docs)
    if total_text < min_chars:
        return False

    # semantic keyword overlap (ignore stopwords)
    question_terms = {
        w for w in question.lower().split()
        if w not in STOPWORDS and len(w) > 2
    }

    if not question_terms:
        return False

    for doc in docs:
        content_terms = set(doc.page_content.lower().split())
        if question_terms & content_terms:
            return True

    return False





def format_citations(docs):
    pages = sorted(
        {
            doc.metadata.get("page")
            for doc in docs
            if doc.metadata.get("page") is not None
        }
    )

    if not pages:
        return "No sources found"

    return "Pages: " + ", ".join(str(p) for p in pages)


def init_rag_runtime():
    embeddings = get_embeddings()
    vectordb = load_vectorstore(embedding=embeddings)

    retriever = DocsVisionRetriever(vectordb, k=5)

    fast_llm = get_fast_llm()   # 🔥 new
    smart_llm = get_llm()       # 70B

    rag_chain = build_rag_chain(
        llm=smart_llm,
        retriever=retriever.retriever,
    )

    return {
        "embeddings": embeddings,
        "vectordb": vectordb,
        "retriever": retriever,
        "fast_llm": fast_llm,
        "smart_llm": smart_llm,
        "rag_chain": rag_chain,
    }

from langchain_core.documents import Document

def ingest_doc_model_into_vectordb(doc_model, vectordb, chunk_size=500):
    blocks = doc_model["blocks"]

    texts = []
    for block in blocks:
        # handle dict-based blocks
        if isinstance(block, dict):
            text = block.get("text", "").strip()
        else:
            text = str(block).strip()

        if text:
            texts.append(text)

    # -------- Chunking --------
    chunks = []
    current = ""

    for text in texts:
        if len(current) + len(text) <= chunk_size:
            current += " " + text
        else:
            chunks.append(current.strip())
            current = text

    if current.strip():
        chunks.append(current.strip())

    # -------- Store --------
    docs = []
    for i, chunk in enumerate(chunks):
        docs.append(
            Document(
                page_content=chunk,
                metadata={"page": i // 3 + 1}
            )
        )

    vectordb.add_documents(docs)

def summarize_document_from_model(doc_model, llm):
    texts = extract_clean_text(doc_model)

    if not texts:
        return "No readable text was found in the document."

    joined = "\n".join(texts[:50])  # limit for safety

    prompt = (
        "Summarize the following document content. "
        "Do NOT describe OCR, metadata, or data structures. "
        "Only summarize the document itself.\n\n"
        + joined
    )

    return llm.invoke(prompt).content




def answer_query_from_ui(question: str, runtime: dict):
    retriever = runtime["retriever"]
    fast_llm = runtime["fast_llm"]
    smart_llm = runtime["smart_llm"]
    rag_chain = runtime["rag_chain"]
    vectordb = runtime["vectordb"]

    # 🔥 PRIORITY 1: META DOCUMENT QUESTIONS (NO INTENT CLASSIFIER)
    if is_meta_document_question(question):
        return summarize_document_from_model(
            session_state.doc_model,
            runtime["smart_llm"]
        )

    # 🔽 ONLY AFTER THAT: intent classification
    intent = classify_intent(fast_llm, question)

    if intent not in {
        "CHAT",
        "GENERAL_KNOWLEDGE",
        "DOC_STRICT",
        "DOC_ASSISTIVE",
    }:
        intent = "DOC_STRICT"

    if intent == "CHAT":
        answer = fast_llm.invoke(question)
        return answer.content

    if intent == "GENERAL_KNOWLEDGE":
        answer = fast_llm.invoke(question)
        return (
            f"{answer.content}\n\n"
            "⚠️ Note: This answer is based on general knowledge, not the document."
        )

    if intent == "DOC_STRICT":
        docs = retriever.retriever.invoke(question)

        result = rag_chain.invoke(question)
        answer_text = result.content if hasattr(result, "content") else str(result)
        sources = format_citations(docs)

        return f"{answer_text}\n\n📚 Sources:\n{sources}"

    if intent == "DOC_ASSISTIVE":
        docs = retriever.retriever.invoke(question)

        assistive_prompt = (
            "The document mentions the topic but does not explain it fully.\n"
            "Provide a clear general explanation.\n"
            "Explicitly state that this explanation is based on general knowledge.\n\n"
            f"Question: {question}"
        )

        answer = fast_llm.invoke(assistive_prompt)

        return (
            f"{answer.content}\n\n"
            f"📚 Document Context:\n{format_citations(docs)}\n\n"
            "⚠️ Note: This explanation is based on general knowledge."
        )
