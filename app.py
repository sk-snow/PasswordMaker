import streamlit as st
from ui.layout import render_layout
from logic.handler import handle_generation

st.set_page_config(page_title="パスワード風味メーカー", layout="centered")
st.title("パスワード風味メーカー")

user_input, min_len, max_len = render_layout()

# 入力が空のときは候補を出さない
if user_input.strip():
    handle_generation(user_input, min_len, max_len)
