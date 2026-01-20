"""
router.py

Responsibility:
- Decide how a query should be handled
"""

from enum import Enum


class QueryRoute(str, Enum):
    CHAT = "chat"
    DOC_STRICT = "doc_strict"
    DOC_TOPIC = "doc_topic"


def route_query(query: str) -> QueryRoute:
    q = query.lower().strip()

    # 1. Greetings / small talk
    greetings = {
        "hi", "hello", "hey", "hii", "yo", "sup"
    }
    if q in greetings:
        return QueryRoute.CHAT

    # 2. Topic / summary style questions
    topic_keywords = [
        "what is this document about",
        "what is the document about",
        "summarize",
        "summary",
        "overall topic",
        "main topic"
    ]
    for kw in topic_keywords:
        if kw in q:
            return QueryRoute.DOC_TOPIC

    # 3. Default: strict document QA
    return QueryRoute.DOC_STRICT
