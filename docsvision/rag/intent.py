"""
intent.py

LLM-based intent classification for DocsVision.
This decides HOW a question should be answered,
not WHAT the answer is.
"""

INTENT_PROMPT = """
You are an intent classifier for a document-based assistant.

Classify the user's question into EXACTLY ONE of the following intents:

- DOC_STRICT: The user wants information strictly from the document.
- DOC_ASSISTIVE: The user wants an explanation of concepts mentioned in the document.
- GENERAL_KNOWLEDGE: The user wants a general explanation and explicitly does NOT want to rely on the document.
- CHAT: Casual conversation or greetings.

Return ONLY the intent name.
Do NOT explain your choice.

User question:
"{question}"
"""


def classify_intent(llm, question: str) -> str:
    """
    Classify user intent using a lightweight LLM call.
    """
    response = llm.invoke(
        INTENT_PROMPT.format(question=question)
    )

    return response.content.strip().upper()
