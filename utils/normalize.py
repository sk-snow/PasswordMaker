import unicodedata

# 全角 → 半角に変換
def to_half_width(text: str) -> str:
    return unicodedata.normalize("NFKC", text)
