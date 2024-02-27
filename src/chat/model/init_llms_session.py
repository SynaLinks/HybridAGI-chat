import streamlit as st
from langchain_mistralai import MistralAIEmbeddings
from langchain_mistralai.chat_models import ChatMistralAI

def init_llms_session():
    cfg = st.session_state.config

    if "embeddings" not in st.session_state.keys():
        st.session_state.embeddings = MistralAIEmbeddings(
            model = cfg.embeddings_model
        )
        st.session_state.embeddings_dim = cfg.embeddings_dim

    if "smart_llm" not in st.session_state.keys():
        st.session_state.smart_llm = ChatMistralAI(
            model = cfg.smart_llm_model,
            temperature = cfg.temperature,
            max_tokens = cfg.max_output_tokens,
            top_p = cfg.top_p,
        )

    if "fast_llm" not in st.session_state.keys():
        st.session_state.fast_llm = ChatMistralAI(
            model = cfg.fast_llm_model,
            temperature = cfg.temperature,
            max_tokens = cfg.max_output_tokens,
            top_p = cfg.top_p,
        )