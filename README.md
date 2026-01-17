📄 DocsVision
Personal Document Reader & Intelligent Explainer

DocsVision is a document intelligence system that converts unstructured documents (PDFs and images) into structured, machine-readable data using Computer Vision, OCR, and layout understanding, and then enables intelligent question-answering using Retrieval-Augmented Generation (RAG).

Instead of manually reading long documents, DocsVision allows users to talk to their documents.

🚀 Project Vision

Most documents are static, unstructured, and hard to query. DocsVision aims to change that by building an end-to-end document understanding pipeline, starting from raw files and ending with intelligent, source-grounded answers.

DocsVision is not just “PDF + LLM”.
It is a layered system that understands what is written, where it is written, and how it is structured before reasoning over it.

🧠 Core Capabilities (V1 Scope – Locked)
✅ Document Ingestion

PDF documents (scanned & digital)

Images (PNG / JPG)

✅ Computer Vision–Based Understanding

High-resolution PDF page rendering

OCR using Tesseract

Word-level bounding boxes

Confidence scores for extracted text

Page-aware extraction

✅ Layout Awareness (V1)

Basic semantic classification:

Headers

Paragraphs

Key-value–like text

Structured JSON output ready for downstream processing

⏳ Intelligence Layer (In Progress)

Layout-aware chunking

Embedding generation (HuggingFace)

Vector storage (ChromaDB)

RAG-based Q&A using open-source LLMs (Groq)

⏳ Product Layer (Planned)

FastAPI backend

Clean frontend UI for upload & chat

Source-grounded answers with citations

🏗️ Architecture Overview (V1)
Document (PDF / Image)
        ↓
Computer Vision Pipeline
(OCR + Bounding Boxes + Layout)
        ↓
Structured JSON Representation
        ↓
Chunking + Embeddings
        ↓
Vector Database (Chroma)
        ↓
RAG Pipeline (LLM)
        ↓
User Q&A Interface

📁 Project Structure
DocsVision/
│
├── docsvision/
│   ├── vision/
│   │   ├── pdf_reader.py        # PDF → images
│   │   ├── image_reader.py      # Image loader
│   │   ├── ocr_engine.py        # OCR + bounding boxes
│   │   ├── layout_utils.py      # Layout heuristics
│   │   └── pipeline.py          # End-to-end CV pipeline
│   │
│   └── __init__.py
│
├── samples/
│   └── sample.pdf
│
├── test_vision.py               # Vision pipeline test
├── pyproject.toml
├── uv.lock
└── README.md

Tech Stack
Computer Vision & OCR

PyMuPDF (PDF rendering)

Tesseract OCR

OpenCV

Pillow

Deep Learning & NLP

PyTorch

Torchvision

HuggingFace Transformers

Sentence Transformers

RAG & Vector Search

LangChain

ChromaDB

Groq LLM API

Backend (Planned)

FastAPI

Uvicorn

Environment Management

uv (locked, reproducible Python environments)

🔒 Environment Setup (Important)

This project uses uv for dependency management.

Install dependencies
uv sync

-->Do NOT

1.Install packages using pip install

2.Modify dependencies without uv add

3.System dependency required:

4.Tesseract OCR (must be installed and accessible)

🛣️ Roadmap
V1 (Current):-

Vision pipeline ✅

Document structure understanding

RAG-based Q&A

V2 (Future):-

More document types (DOCX, PPTX)

Advanced layout models

Persistent memory

Multi-document reasoning
