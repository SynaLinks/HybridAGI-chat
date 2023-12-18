import os
import streamlit as st
from hybridagi.config import Config

def init_config():
    if "config" not in st.session_state.keys():
        st.session_state.config = Config()

    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    if os.environ["OPENAI_API_KEY"] == "your-openai-api-key" and \
        st.session_state.config.private_mode == False:
        st.warning("Please provide your OpenAI API key or switch to private mode")