from pathlib import Path
import json

from docsvision.vision.pdf_reader import pdf_to_images
from docsvision.vision.image_reader import load_image
from docsvision.vision.ocr_engine import extract_text_with_boxes
from docsvision.vision.layout_utils import classify_block


def process_document(path):
    path = str(path)
    if path.lower().endswith(".pdf"):
        images = pdf_to_images(path)
    else:
        images = [load_image(path)]

    document = []

    for page_no, img in enumerate(images, start=1):
        blocks = extract_text_with_boxes(img)

        for block in blocks:
            block["page"] = page_no
            block["block_type"] = classify_block(block)

        document.extend(blocks)

    return document


def main():
    print("🚀 Running vision pipeline...")

    raw_dir = Path("docsvision/data/raw_docs")
    parsed_dir = Path("docsvision/data/parsed_docs")
    parsed_dir.mkdir(parents=True, exist_ok=True)

    SUPPORTED_EXTENSIONS = {".pdf" , ".png" , ".jpeg" , ".jpg"}

    files = [
        f for f in raw_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    print(f"📂 Found {len(files)} raw files")

    for file_path in files:
        print(f"➡️ Processing {file_path.name}")

        blocks = process_document(str(file_path))

        output = {
            "source": file_path.name,
            "blocks": blocks,
        }

        output_path = parsed_dir / f"{file_path.stem}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {output_path}")

    print("🎉 Vision pipeline completed")


if __name__ == "__main__":
    main()

