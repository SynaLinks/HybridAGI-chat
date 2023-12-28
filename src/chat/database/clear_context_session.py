import streamlit as st

def clear_context_session():
    if "filesystem_context" in st.session_state.keys():
        del st.session_state["filesystem_context"]