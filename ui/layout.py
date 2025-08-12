import streamlit as st

def render_layout():
    st.markdown("**好きなワードを入れてね**")

    # フラグで初期化
    if "clear_triggered" not in st.session_state:
        st.session_state["clear_triggered"] = False

    if st.session_state["clear_triggered"]:
        st.session_state["user_input"] = ""
        st.session_state["clear_triggered"] = False
        st.rerun()

    # 入力欄
    user_input = st.text_input(
        label="",
        placeholder="英字で入力してください (例: wordなど)",
        key="user_input"
    )

    # ボタンを右寄せ配置
    col = st.columns([1, 5, 1])
    with col[2]:
        if st.button("× クリア", use_container_width=True):
            st.session_state["clear_triggered"] = True

    min_len = st.number_input("出力の最小文字数", min_value=4, max_value=64, value=4)
    max_len = st.number_input("出力の最大文字数", min_value=4, max_value=64, value=8)

    return user_input,  min_len, max_len
