import streamlit as st

def clear_database_session():
    if "filesystem" in st.session_state.keys():
        del st.session_state["filesystem"]
    if "program_memory" in st.session_state.keys():
        del st.session_state["program_memory"]
    if "trace_memory" in st.session_state.keys():
        del st.session_state["trace_memory"]