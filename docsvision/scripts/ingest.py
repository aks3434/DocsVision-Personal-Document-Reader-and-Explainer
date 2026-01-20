"""
ingest.py

Usage:
python scripts/ingest.py data/parsed_docs/sample.json
"""

import sys
import json
from pathlib import Path

from docsvision.core.chunking import Chunker
from docsvision.core.embedding import get_embeddings
from docsvision.core.vectordb import get_vectorstore


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/ingest.py <parsed_json_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        raise FileNotFoundError(f"{json_path} does not exist")

    with open(json_path, "r", encoding="utf-8") as f:
        parsed_doc = json.load(f)

    source_name = json_path.stem

    print("🔹 Chunking document...")
    chunker = Chunker()
    chunks = chunker.build_chunks(parsed_doc, source_name)

    print(f"✅ Created {len(chunks)} chunks")

    print("🔹 Loading embeddings...")
    embeddings = get_embeddings()

    print("🔹 Storing vectors in ChromaDB...")
    vectordb = get_vectorstore(
        documents=chunks,
        embedding=embeddings,
    )

    print("✅ Ingestion complete")
    print(f"📦 Total vectors in DB: {vectordb._collection.count()}")


if __name__ == "__main__":
    main()
