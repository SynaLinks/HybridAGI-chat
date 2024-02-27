import os
import streamlit as st
from hybridagi.config import Config

def init_config():
    if "config" not in st.session_state.keys():
        st.session_state.config = Config()
    if "MISTRAL_API_KEY" not in os.environ:
        os.environ["MISTRAL_API_KEY"] = "your-api-key"
    if os.environ["MISTRAL_API_KEY"] == "your-api-key" and \
        not st.session_state.config.private_mode:
        st.warning("Please provide your [MistralAI](https://mistral.ai/) API key in the settings tab")