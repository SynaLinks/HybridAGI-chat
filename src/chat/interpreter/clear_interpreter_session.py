import streamlit as st

def clear_interpreter_session():
    if "interpreter" in st.session_state.keys():
        del st.session_state["interpreter"]