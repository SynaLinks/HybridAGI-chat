import streamlit as st
from .clear_model_session import clear_model_session

def display_settings():
    save = st.button(
        label="Apply settings",
        help="Reset your session to apply your new settings")
    if save:
        clear_model_session()
    
    cfg = st.session_state.config
    # Private mode toggle
    with st.expander("**LLM provider settings**"):
        st.session_state.config.private_mode = st.toggle(
            label="Use Private Mode",
            help="Use Text Generation endpoint instead of OpenAI",
        )
        # OpenAI API key
        st.write("**OpenAI settings**")
        openai_api_key = st.text_input(
            label="OpenAI API key",
            help="Used when private mode is disabled",
            type="password",
            value=st.session_state.config.openai_api_key)
        if openai_api_key:
            st.session_state.config.openai_api_key = openai_api_key
        st.session_state.config.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
        )
        st.session_state.config.smart_llm_model = st.text_input(
            label="Smart LLM model",
            value=st.session_state.config.smart_llm_model)
        st.session_state.config.fast_llm_model = st.text_input(
            label="Fast LLM model",
            value=st.session_state.config.fast_llm_model)

        st.write("**Text Generation settings**")
        # Local model URL
        st.session_state.config.local_smart_llm_model_url = st.text_input(
            label="Local smart LLM model URL",
            help="Used when private mode is enabled",
            value=st.session_state.config.local_smart_llm_model_url)
        st.session_state.config.local_fast_llm_model_url = st.text_input(
            label="Local fast LLM model URL",
            help="Used when private mode is enabled",
            value=st.session_state.config.local_fast_llm_model_url)
    # Redis URL
    with st.expander("**Database settings**"):
        st.session_state.config.redis_url = st.text_input(
            label="FalkorDB URL",
            help="The URL of the vector/graph database",
            value=st.session_state.config.redis_url)
    # HybridAGI settings
    with st.expander("**HybridAGI settings**"):
        st.session_state.config.downloads_directory = st.text_input(
            label="Downloads directory",
            help="This is where the AI upload its work",
            value=st.session_state.config.downloads_directory,
        )
        st.session_state.config.documentation_directory = st.text_input(
            label="Documentation directory",
            help="This is where the AI get its unstructured knowledge",
            value=st.session_state.config.documentation_directory,
        )
        st.session_state.config.library_directory = st.text_input(
            label="Library directory",
            help="This is where the AI get its Cypher programs",
            value=st.session_state.config.library_directory,
        )
        st.session_state.config.chunk_size = st.slider(
            "Chunk size",
            min_value=1000,
            max_value=4000,
            value=1500,
            help="Used to chunk documents into manageable size",
        )

        st.session_state.config.chunk_overlap = st.slider(
            "Chunk overlap",
            min_value=0,
            max_value=1000,
            value=0,
            help="Used to chunk documents into manageable size",
        )
        
        st.session_state.config.max_iteration = st.slider(
            "Max iteration",
            min_value=0,
            max_value=2000,
            value=100,
            help="The maximum iteration per run",
        )

        st.session_state.config.max_decision_attemps = st.slider(
            "Max decision attemps",
            min_value=1,
            max_value=10,
            value=5,
            help="The maximum decision attemps before raising an exception",
        )

        st.session_state.config.max_evaluation_attemps = st.slider(
            "Max evaluation attemps",
            min_value=1,
            max_value=10,
            value=5,
            help="The maximum evaluation attemps before raising an exception",
        )
