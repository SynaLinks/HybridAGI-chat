import streamlit as st

def display_answer_input():
    # User-provided prompt
    if response := st.chat_input("Enter your response (use `/stop` if you want to stop the AI at any time)"):
        if "request_answer" not in st.session_state.keys():
            st.session_state.request_answer = False
        if st.session_state.request_answer:
            st.session_state.messages.append({"role": "user", "content": response})
            st.session_state.answer = response
        if response == "/stop":
            st.session_state.stop = True