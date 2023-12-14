import streamlit as st
from hybridagi.config import Config

def init_config():
    if "config" not in st.session_state.keys():
        st.session_state.config = Config()

    if st.session_state.config.openai_api_key == "your-openai-api-key" and \
        st.session_state.config.private_mode == False:
        st.warning("Please provide your OpenAI API key or switch to private mode")
