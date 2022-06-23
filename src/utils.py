from unicodedata import normalize

def remove_accentuation(text: str) -> str:
    return normalize("NFD", text.lower().strip()).encode("ascii", "ignore").decode("utf-8")