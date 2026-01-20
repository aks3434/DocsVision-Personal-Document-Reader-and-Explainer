"""
prompts.py

Responsibility:
- Centralized prompt templates for DocsVision RAG
"""

from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """
You are DocsVision, an AI document assistant.

Rules you MUST follow:
- Answer ONLY using the provided context.
- If the answer is not in the context, say: "I don't know based on the document."
- Do NOT use external knowledge.
- Be clear, concise, and factual.
- Cite page numbers when relevant.
"""


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            """
Context:
{context}

Question:
{question}

Answer:
""",
        ),
    ]
)
