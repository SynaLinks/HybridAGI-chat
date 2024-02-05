import streamlit as st
from langchain_together import Together
from langchain_together.embeddings import TogetherEmbeddings

def init_llms_session():
    cfg = st.session_state.config

    if "embeddings" not in st.session_state.keys():
        st.session_state.embeddings = TogetherEmbeddings(
            model=cfg.embeddings_model
        )
        st.session_state.embeddings_dim = cfg.embeddings_dim

    if "smart_llm" not in st.session_state.keys():
        st.session_state.smart_llm = Together(
            model=cfg.smart_llm_model,
            temperature=cfg.temperature,
            max_tokens=cfg.max_output_tokens,
            top_p=cfg.top_p,
            top_k=cfg.top_k,
            repetition_penalty = cfg.repetition_penalty,
        )

    if "fast_llm" not in st.session_state.keys():
        st.session_state.fast_llm = Together(
            model=cfg.fast_llm_model,
            temperature=cfg.temperature,
            max_tokens=cfg.max_output_tokens,
            top_p=cfg.top_p,
            top_k=cfg.top_k,
            repetition_penalty = cfg.repetition_penalty,
        )