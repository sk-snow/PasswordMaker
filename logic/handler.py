import streamlit as st
from utils.normalize import to_half_width
from utils.stylizer import stylize_word
from components.copy_button import copy_button_row

def _validate(word_len: int, min_len: int, max_len: int):
    if min_len > max_len:
        return "最小文字数が最大文字数を超えています。"
    if min_len < 1:
        return "最小文字数は1以上にしてください。"
    if word_len > max_len:
        return f"単語が長すぎます（{word_len}>{max_len}）"
    return None

def handle_generation(user_input: str, min_len: int, max_len: int):
    if not user_input.strip():
        return

    normalized = to_half_width(user_input.strip())
    err = _validate(len(normalized), min_len, max_len)
    if err:
        st.warning(err)
        return

    st.subheader("候補：")
    for pw in stylize_word(normalized, 5, min_len, max_len):  # sym=削除
        copy_button_row(pw)