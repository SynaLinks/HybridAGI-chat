import streamlit as st

def clear_database_session():
    if "program_memory" in st.session_state.keys():
        del st.session_state["program_memory"]
    if "trace_memory" in st.session_state.keys():
        del st.session_state["trace_memory"]
    if "interpreter" in st.session_state.keys():
        del st.session_state["interpreter"]