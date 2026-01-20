"""
retriever.py

Responsibility:
- Retrieve relevant document chunks from vector store
"""

from typing import List
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore


class DocsVisionRetriever:
    def __init__(
        self,
        vectorstore: VectorStore,
        k: int = 5,
        search_type: str = "similarity",
    ):
        self.vectorstore = vectorstore
        self.k = k
        self.search_type = search_type

        self.retriever = vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k},
        )

    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve top-k relevant document chunks.
        """
        return self.retriever.invoke(query)
