from __future__ import annotations

from typing import Dict


def classify_block_type(blocks):
    """
    Classify blocks based on text-only heuristics.
    blocks: list[str]
    """

    classified = []

    for text in blocks:
        t = text.strip()

        if not t:
            continue

        if t.isupper() and len(t) < 100:
            block_type = "heading"
        elif len(t) < 50:
            block_type = "short_text"
        else:
            block_type = "paragraph"

        classified.append({
            "text": t,
            "type": block_type
        })

    return classified

