import re

def clean_text(text: str) -> str:
    """
    Clean input text: lowercasing, remove punctuation, normalize whitespace.
    """
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    # Remove punctuation and special characters, keep alphanumeric and spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text