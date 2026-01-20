from .blocks import normalize_ocr_output
from .layout import classify_block_type


def build_document_model(ocr_result):
    page_blocks = normalize_ocr_output(ocr_result)

    flat_blocks = [
        text
        for page in page_blocks
        for text in page
        if text.strip()
    ]

    layout = classify_block_type(flat_blocks)

    return {
        "blocks": flat_blocks,      # list[str]
        "pages": page_blocks,       # list[list[str]]
        "layout": layout            # list[dict]
    }
