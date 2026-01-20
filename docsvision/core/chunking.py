"""
chunking.py

Responsibility:
- Convert DocsVision parsed JSON into LangChain Documents
- Apply text chunking
- Preserve metadata for retrieval & citation
"""

from typing import List, Dict
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
        )

    def json_to_documents(
    self,
    parsed_json: Dict,
    source_name: str,
) -> List[Document]:

        documents: List[Document] = []

        blocks = parsed_json.get("blocks", [])

        buffer = []
        current_page = None

        for block in blocks:
            text = block.get("text", "").strip()
            page = block.get("page")

            if not text:
                continue

            # New page → flush buffer
            if current_page is not None and page != current_page:
                combined_text = " ".join(buffer).strip()
                if len(combined_text) > 100:
                    documents.append(
                        Document(
                            page_content=f"[Page {current_page}]\n{combined_text}",
                            metadata={
                                "page": current_page,
                                "source": source_name,
                         },
                        )
                     )
                buffer = []

            current_page = page
            buffer.append(text)

        # Flush last page
        if buffer:
            combined_text = " ".join(buffer).strip()
            if len(combined_text) > 20:
                documents.append(
                    Document(
                        page_content=f"[Page {current_page}]\n{combined_text}",
                        metadata={
                            "page": current_page,
                            "source": source_name,
                        },
                    )
                )

        return documents



    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits documents into semantically meaningful chunks.
        """
        chunks = self.splitter.split_documents(documents)
        return chunks

    def build_chunks(
        self,
        parsed_json: Dict,
        source_name: str,
    ) -> List[Document]:
        """
        End-to-end helper:
        JSON -> Documents -> Chunks
        """
        documents = self.json_to_documents(parsed_json, source_name)
        chunks = self.chunk_documents(documents)
        return chunks
