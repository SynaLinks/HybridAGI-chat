import streamlit as st
from .clear_database import clear_database

def clear_model_session():
    clear_database()
    if "embeddings" in st.session_state.keys():
        del st.session_state["embeddings"]
    if "smart_llm" in st.session_state.keys():
        del st.session_state["smart_llm"]
    if "fast_llm" in st.session_state.keys():
        del st.session_state["fast_llm"]
    if "filesystem" in st.session_state.keys():
        del st.session_state["filesystem"]
    if "filesystem_context" in st.session_state.keys():
        del st.session_state["filesystem_context"]
    if "program_memory" in st.session_state.keys():
        del st.session_state["program_memory"]
    if "trace_memory" in st.session_state.keys():
        del st.session_state["trace_memory"]
    if "interpreter" in st.session_state.keys():
        del st.session_state["interpreter"]

    
