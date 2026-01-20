from __future__ import annotations

import uuid
from typing import Dict, List


def _clean_text(text: str) -> str:
    """
    Basic OCR text cleanup.
    Extend later (hyphenation, unicode fixes, etc.).
    """
    if not text:
        return ""
    return " ".join(text.strip().split())


def normalize_ocr_output(
    raw_ocr: List[Dict]
) -> List[Dict]:
    """
    Convert raw OCR output into normalized document blocks.

    Parameters
    ----------
    raw_ocr : List[Dict]
        Raw OCR results from vision layer.

    Returns
    -------
    List[Dict]
        Normalized document blocks.
    """
    normalized_blocks: List[Dict] = []

    for item in raw_ocr:
        text = _clean_text(item.get("text", ""))
        if not text:
            continue  # skip empty OCR noise

        block = {
            "id": str(uuid.uuid4()),
            "text": text,
            "bbox": item.get("bbox"),
            "page": item.get("page", 1),
            "confidence": float(item.get("confidence", 0)) / 100.0,
            "block_type": "unknown"
        }

        normalized_blocks.append(block)

    return normalized_blocks
