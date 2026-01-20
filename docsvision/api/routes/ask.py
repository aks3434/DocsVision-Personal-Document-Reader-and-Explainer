from fastapi import APIRouter
from pydantic import BaseModel

from docsvision.core.embedding import get_embeddings
from docsvision.core.vectordb import load_vectorstore
from docsvision.core.retriever import DocsVisionRetriever
from docsvision.core.llm import get_llm
from docsvision.rag.chain import build_rag_chain
from docsvision.rag.intent import classify_intent
from docsvision.scripts.query import (
    is_context_sufficient,
    format_citations,
)

router = APIRouter()

# 🔒 Load ONCE (important)
embeddings = get_embeddings()
vectordb = load_vectorstore(embedding=embeddings)
retriever = DocsVisionRetriever(vectordb)
llm = get_llm()
rag_chain = build_rag_chain(llm, retriever.retriever)

class AskRequest(BaseModel):
    question: str

@router.post("/")
def ask_question(req: AskRequest):
    question = req.question.strip()

    if not question:
        return {"answer": "Please ask a valid question."}

    intent = classify_intent(llm, question)

    # 🔹 GENERAL KNOWLEDGE
    if intent == "GENERAL_KNOWLEDGE":
        return {
            "answer": llm.invoke(question).content,
            "note": "General knowledge (not document-based)"
        }

    # 🔹 Retrieve once
    docs = retriever.retriever.invoke(question)

    # 🔹 STRICT DOCUMENT QA
    if intent == "DOC_STRICT":
        if not is_context_sufficient(docs, question):
            return {
                "answer": "The requested information is not found in the document.",
                "sources": []
            }

        return {
            "answer": rag_chain.invoke(question),
            "sources": format_citations(docs)
        }

    # 🔹 ASSISTIVE MODE
    if intent == "DOC_ASSISTIVE":
        assistive_prompt = (
            "Provide a clear general explanation.\n"
            "Explicitly state this is based on general knowledge.\n\n"
            f"Question: {question}"
        )

        return {
            "answer": llm.invoke(assistive_prompt).content,
            "sources": format_citations(docs),
            "note": "General explanation inspired by document context"
        }

    # 🔹 Fallback
    return {"answer": "I could not understand the request."}
