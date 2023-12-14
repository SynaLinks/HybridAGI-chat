import streamlit as st

def clear_database():
    st.session_state.program_memory.clear()
    st.session_state.filesystem.clear()