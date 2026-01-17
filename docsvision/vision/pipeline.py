from docsvision.vision.pdf_reader import pdf_to_images
from docsvision.vision.image_reader import load_image
from docsvision.vision.ocr_engine import extract_text_with_boxes
from docsvision.vision.layout_utils import classify_block

def process_document(path):
    if path.lower().endswith(".pdf"):
        images = pdf_to_images(path)
    else:
        images = [load_image(path)]

    document = []

    for page_no, img in enumerate(images, start=1):
        blocks = extract_text_with_boxes(img)

        for block in blocks:
            block["page"] = page_no
            block["type"] = classify_block(block)

        document.extend(blocks)

    return document
