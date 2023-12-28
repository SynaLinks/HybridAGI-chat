import streamlit as st

def clear_messages():
    st.session_state.messages = []
    st.session_state.answer = ""
    st.session_state.request_answer = False
