from docsvision.rag.router import route_query, QueryRoute
from docsvision.core.retriever import DocsVisionRetriever

def build_prompt(context_docs, query, route):
    context_text = "\n\n".join(d.page_content for d in context_docs)

    if route == QueryRoute.DOC_TOPIC:
        system = (
            "Summarize the document. "
            "Focus on the main idea, purpose, and key sections."
        )
    else:
        system = (
            "Answer the question strictly using the document context. "
            "If the answer is not present, say so."
        )

    return f"""
SYSTEM:
{system}

CONTEXT:
{context_text}

QUESTION:
{query}

ANSWER:
""".strip()


def run_docsvision_query(
    query: str,
    vectorstore,
    llm
):
    """
    Single entry point for DocsVision intelligence
    """

    route = route_query(query)

    # 1️⃣ Chat mode
    if route == QueryRoute.CHAT:
        return llm.invoke(query)

    # 2️⃣ Document modes
    k = 10 if route == QueryRoute.DOC_TOPIC else 4

    retriever = DocsVisionRetriever(
        vectorstore=vectorstore,
        k=k
    )

    context_docs = retriever.retrieve(query)

    prompt = build_prompt(
        context_docs=context_docs,
        query=query,
        route=route
    )

    return llm.invoke(prompt)


