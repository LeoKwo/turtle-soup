import streamlit as st


if "game_info" not in st.session_state:
    st.session_state.game_info = {}

with st.chat_message("ai"):
    st.markdown("#### 海龟汤汤面")
    st.markdown(st.session_state.game_info['soup'])
if prompt := st.chat_input("向主持人提问。"):
    with st.chat_message("user"):
        st.markdown(prompt)