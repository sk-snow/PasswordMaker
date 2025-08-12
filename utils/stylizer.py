import random
import string

_CHAR = {
    'a': ['@', '4'],
    'b': ['8', '13'],
    'e': ['3'],
    'i': ['1'],
    'o': ['0'],
    's': ['5', 'z', 'Z'],
    't': ['7'],
    'l': ['1'],
    'g': ['9'],
    'h': ['#'],
    'z': ['2']
}

def _rand_upper(s, rate=0.3):
    return ''.join(
        c.upper() if c.isalpha() and random.random() < rate else c
        for c in s
    )

def _stylize_base(word):
    return ''.join(
        random.choice(_CHAR[c.lower()]) if c.lower() in _CHAR and random.random() < 0.7 else c
        for c in word
    )

def stylize_word(word, v, min_total_len, max_total_len, sym=""):
    out = []
    for _ in range(v):
        total_len = random.randint(min_total_len, max_total_len)

        if not sym:
            # 記号なし：語尾なし、長さ調整のみ（数値追加）
            base = _stylize_base(word)
            base = _rand_upper(base)
            if len(base) > total_len:
                base = base[:total_len]
            elif len(base) < total_len:
                digits = ''.join(random.choices(string.digits, k=total_len - len(base)))
                base += digits
            out.append(base)
        else:
            # 記号あり：語尾付き（記号＋数字をランダム混合）
            suffix_len = random.randint(1, total_len - 1)
            base_max = total_len - suffix_len
            base = _rand_upper(_stylize_base(word)[:base_max])
            pool = [
                random.choice(sym) if random.random() < 0.6 else random.choice(string.digits)
                for _ in range(suffix_len)
            ]
            suffix = ''.join(pool)
            out.append(base + suffix)

    return out
