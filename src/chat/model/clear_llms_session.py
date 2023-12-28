import streamlit as st

def clear_llms_session():
    if "embeddings" in st.session_state.keys():
        del st.session_state["embeddings"]
    if "smart_llm" in st.session_state.keys():
        del st.session_state["smart_llm"]
    if "fast_llm" in st.session_state.keys():
        del st.session_state["fast_llm"]