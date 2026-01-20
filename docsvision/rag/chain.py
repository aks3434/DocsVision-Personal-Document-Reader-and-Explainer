"""
chain.py

Responsibility:
- Assemble Retrieval-Augmented Generation pipeline
"""

from typing import Dict, Any, List

from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from docsvision.rag.prompts import RAG_PROMPT


def format_context(documents: List[Document]) -> str:
    """
    Convert retrieved documents into readable context for the LLM.
    """
    formatted_chunks = []

    for doc in documents:
        page = doc.metadata.get("page", "N/A")
        source = doc.metadata.get("source", "unknown")

        formatted_chunks.append(
            f"[Source: {source}, Page: {page}]\n{doc.page_content}"
        )

    return "\n\n".join(formatted_chunks)


def build_rag_chain(llm, retriever):
    """
    Build the RAG chain using LangChain LCEL.
    """

    rag_chain = (
        {
            "context": retriever | format_context,
            "question": RunnablePassthrough(),
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return rag_chain
