import streamlit as st
from hybridagi import FileSystemContext

def init_context_session():
    if "filesystem_context" not in st.session_state.keys():
        st.session_state.filesystem_context = FileSystemContext()