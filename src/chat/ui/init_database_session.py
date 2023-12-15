import streamlit as st
import numpy as np
from hybridagi import FileSystemContext, FileSystem, ProgramMemory, TraceMemory

def _normalize_vector(value):
    return np.add(np.divide(value, 2), 0.5)
    
def init_database_session() -> bool:
    cfg = st.session_state.config

    if "filesystem_context" not in st.session_state.keys():
        st.session_state.filesystem_context = FileSystemContext()
    try:
        if "filesystem" not in st.session_state.keys():
            st.session_state.filesystem = FileSystem(
                redis_url = cfg.redis_url,
                index_name = cfg.memory_index,
                embeddings = st.session_state.embeddings,
                embeddings_dim = st.session_state.embeddings_dim,
                normalize = _normalize_vector,
                context = st.session_state.filesystem_context)
            st.session_state.filesystem.initialize()

        if "program_memory" not in st.session_state.keys():
            st.session_state.program_memory = ProgramMemory(
                redis_url = cfg.redis_url,
                index_name = cfg.memory_index,
                embeddings = st.session_state.embeddings,
                embeddings_dim = st.session_state.embeddings_dim,
                normalize = _normalize_vector)
            st.session_state.program_memory.initialize()

        if "trace_memory" not in st.session_state.keys():
            st.session_state.trace_memory = TraceMemory(
                redis_url = cfg.redis_url,
                index_name = cfg.memory_index,
                embeddings = st.session_state.embeddings,
                embeddings_dim = st.session_state.embeddings_dim,
                normalize = _normalize_vector)
            st.session_state.trace_memory.initialize()
        return True
    except Exception:
        st.error("Could not connect to FalkorDB database, please ensure you have the correct URL and the server is up.")
        return False