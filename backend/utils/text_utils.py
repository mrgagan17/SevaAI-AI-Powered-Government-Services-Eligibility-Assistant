import re
import unicodedata

def clean_text(text: str) -> str:
    """Clean and normalize extracted PDF text."""
    if not text:
        return ""
    # Normalize unicode
    text = unicodedata.normalize('NFKD', text)
    # Remove multiple spaces/newlines while retaining paragraph separation
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def sanitize_filename(filename: str) -> str:
    """Sanitize uploaded document filenames to prevent directory traversal or unsafe chars."""
    filename = re.sub(r'[^\w\s\.-]', '', filename)
    filename = filename.replace(' ', '_')
    return filename or "document.pdf"
