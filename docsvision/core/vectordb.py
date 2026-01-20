"""
vectordb.py

Responsibility:
- Create / load ChromaDB vector store
- Ensure persistence
"""

from typing import List
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


def get_vectorstore(
    documents: List[Document],
    embedding: Embeddings,
    persist_directory: str = "storage/chroma",
    collection_name: str = "docsvision",
) -> Chroma:
    """
    Create or load a Chroma vector store.

    Args:
        documents: Chunked LangChain Documents
        embedding: Embedding function
        persist_directory: Directory for persistence
        collection_name: Chroma collection name

    Returns:
        Chroma vector store
    """

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )

    vectordb.persist()
    return vectordb


def load_vectorstore(
    embedding: Embeddings,
    persist_directory: str = "storage/chroma",
    collection_name: str = "docsvision",
) -> Chroma:
    """
    Load an existing Chroma vector store from disk.
    """

    return Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )
