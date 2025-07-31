import streamlit as st
import streamlit.components.v1 as components
import random
import string
import unicodedata
import html

# ---------- 変換用マップ ----------
char_map = {
    'a': ['@', '4'],
    'b': ['8', '13'],
    'e': ['3', '€'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['$', '5', 'z', 'Z'],
    't': ['7', '+'],
    'l': ['1', '|'],
    'g': ['9'],
    'h': ['#'],
    'z': ['2']
}

# ---------- 全角→半角 ----------
def to_half_width(text):
    return unicodedata.normalize('NFKC', text)

# ---------- ランダムで一部大文字 ----------
def random_uppercase(word, ratio=0.3):
    return ''.join(
        c.upper() if c.isalpha() and random.random() < ratio else c
        for c in word
    )

# ---------- ランダム語尾 ----------
def random_suffix(min_len=8, max_len=12, symbol_pool="!@#$%^&*"):
    suffix_len = random.randint(min_len, max_len)
    combined_pool = string.digits + symbol_pool
    return ''.join(random.choices(combined_pool, k=suffix_len))

# ---------- パスワード風変換 ----------
def stylize_word(word, variations=3, min_len=8, max_len=12, symbol_pool="!@#$%^&*"):
    results = []
    for _ in range(variations):
        styled = ""
        for c in word:
            if c.lower() in char_map and random.random() < 0.7:
                styled += random.choice(char_map[c.lower()])
            else:
                styled += c
        styled = random_uppercase(styled)
        styled += random_suffix(min_len, max_len, symbol_pool)
        results.append(styled)
    return results

# ---------- コピーボタン付き表示 ----------
def copy_button_row(text, label="コピー"):
    display = html.escape(text, quote=True)  # 表示用
    btn_id = f"btn_{random.randint(0, 1_000_000)}"
    components.html(
        f"""
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <code style="flex: 1; font-size: 16px;">{display}</code>
            <button id="{btn_id}" style="margin-left: 10px;">{label}</button>
        </div>
        <script>
            const btn = document.getElementById("{btn_id}");
            btn.addEventListener("click", () => {{
                navigator.clipboard.writeText("{text}");
                btn.textContent = "コピー済み";
                setTimeout(() => btn.textContent = "{label}", 1000);
            }});
        </script>
        """,
        height=50,
    )

#  タイトル 
st.title("パスワード風味メーカー")

# ラベル部分
st.markdown("**好きなワードを入れてね**")

# フォーム＋ボタンを並列に表示
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        label="",  # ラベルは空文字に
        placeholder="英数字で入力してください (例: white, bear など)",
        key="user_input"
    )

with col2:
    if st.button("× クリア"):
        st.session_state["user_input"] = ""
        st.rerun()


# 記号・長さ指定UI
custom_symbols = st.text_input(
    "使用したい記号の種類を指定（空欄でもOK）",
    placeholder="!@#$%^&*"
)

min_len = st.number_input("パスワードの最小文字数（語尾）", value=4, min_value=1, max_value=32)
max_len = st.number_input("パスワードの最大文字数（語尾）", value=8, min_value=1, max_value=64)

# 入力・設定チェック
if min_len > max_len:
    st.error("最小文字数が最大文字数を超えています。")

elif user_input:
    normalized = to_half_width(user_input)
    word_len = len(normalized)

    if word_len > max_len:
        st.warning(f"単語の長さ（{word_len}文字）が、最大パスワード長({max_len})を超えています。")
    elif word_len + min_len > max_len:
        st.warning(
            f"単語（{word_len}文字）+ 語尾の最小長({min_len}) = {word_len + min_len}文字 が、最大長({max_len})を超えます。\n"
            "最大長の設定を増やすか、単語を短くしてください。"
        )
    else:
        st.subheader("候補：")
        for p in stylize_word(
            normalized,
            variations=5,
            min_len=min_len,
            max_len=max_len,
            symbol_pool=custom_symbols.strip() if custom_symbols.strip() else ""
        ):
            copy_button_row(p)
