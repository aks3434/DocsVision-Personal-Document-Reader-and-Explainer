from .blocks import normalize_ocr_output
from .layout import classify_block_type


from .blocks import normalize_ocr_output
from .layout import classify_block_type


def build_document_model(ocr_result):
    """
    Build a clean document model from OCR output.

    Output contract:
    - blocks   : List[str]   (TEXT ONLY — no OCR metadata)
    - pages    : Dict[int, List[str]]
    - sections : List[Dict]  (optional / future use)
    """

    # 1️⃣ Normalize raw OCR output into structured blocks
    normalized_blocks = normalize_ocr_output(ocr_result)

    # 2️⃣ Extract TEXT ONLY (🔥 this is the critical fix)
    blocks = [b["text"] for b in normalized_blocks if b.get("text")]

    # 3️⃣ Build page-wise structure (simple & safe)
    pages = {}
    for b in normalized_blocks:
        page = b.get("page", 1)
        text = b.get("text", "").strip()

        if not text:
            continue

        if page not in pages:
            pages[page] = []

        pages[page].append(text)

    # 4️⃣ Optional: classify layout (kept for future UI / logic)
    # Currently not used downstream, but safe to compute
    sections = classify_block_type(
        [b["text"] for b in normalized_blocks if b.get("text")]
    )

    # 5️⃣ Final document model (🔥 CLEAN CONTRACT)
    doc_model = {
        "blocks": blocks,     # ✅ List[str]
        "pages": pages,       # ✅ Dict[int, List[str]]
        "sections": sections  # ✅ Optional metadata
    }

    return doc_model
