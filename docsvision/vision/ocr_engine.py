import pytesseract
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_with_boxes(image):
    data = pytesseract.image_to_data(
        image, output_type=pytesseract.Output.DATAFRAME
    )

    data = data.dropna()
    blocks = []

    for _, row in data.iterrows():
        if row.text.strip():
            blocks.append({
                "text": row.text,
                "bbox": [
                    int(row.left),
                    int(row.top),
                    int(row.left + row.width),
                    int(row.top + row.height),
                ],
                "confidence": float(row.conf),
            })

    return blocks
