import streamlit as st

def init_chat_messages():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = []
    if "answer" not in st.session_state.keys():
        st.session_state.answer = ""
    if "waiting_answer" not in st.session_state.keys():
        st.session_state.waiting_answer = False
    if "stop" not in st.session_state.keys():
        st.session_state.stop = False