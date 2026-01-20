"""
llm.py

Responsibility:
- Initialize Groq LLM for DocsVision
- Load API key from .env
"""

import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel


# Load environment variables from .env
load_dotenv()


def get_llm(
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.0,
) -> BaseChatModel:
    """
    Returns a Groq Chat LLM.

    Requires:
        GROQ_API_KEY in .env file

    Args:
        model: Groq-supported model name
        temperature: Controls randomness (0.0 = deterministic)

    Returns:
        BaseChatModel
    """

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. Please set it in your .env file."
        )

    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=api_key,
    )

def get_fast_llm(
    temperature: float = 0.0,
) -> BaseChatModel:
    """
    Returns a fast, low-latency Groq Chat LLM.
    Used for intent classification and general chat.
    """

    return get_llm(
        model="llama-3.1-8b-instant",
        temperature=temperature,
    )

