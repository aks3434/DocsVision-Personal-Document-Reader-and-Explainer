"""
embedding.py

Responsibility:
- Initialize HuggingFace embeddings for DocsVision
"""

from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
):
    """
    Returns a HuggingFaceEmbeddings instance.

    Args:
        model_name: Explicit HF embedding model

    Returns:
        HuggingFaceEmbeddings
    """
    return HuggingFaceEmbeddings(model_name=model_name)
