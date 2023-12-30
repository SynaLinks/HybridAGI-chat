import streamlit as st

def display_answer_input():
    # User-provided prompt
    response = st.chat_input("Enter your answer")
    if response:
        st.session_state.messages.append({"role": "user", "content": response})
        st.session_state.answer = response
        st.rerun()