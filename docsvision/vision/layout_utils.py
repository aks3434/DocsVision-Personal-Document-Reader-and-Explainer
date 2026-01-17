def classify_block(block):
    text = block["text"]

    if text.isupper() and len(text) > 6:
        return "header"
    elif any(char.isdigit() for char in text):
        return "key_value"
    else:
        return "paragraph"
