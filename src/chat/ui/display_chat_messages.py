import streamlit as st

def display_chat_messages():
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] in ["ai", "assistant"]:
            with st.chat_message(message["role"], avatar="img/logo.png"):
                st.write(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.write(message["content"])