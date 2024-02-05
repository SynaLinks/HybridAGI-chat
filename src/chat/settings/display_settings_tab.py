import os
import streamlit as st

from ..model.clear_llms_session import clear_llms_session
from ..database.clear_database_session import clear_database_session
from ..database.clear_context_session import clear_context_session
from ..interpreter.clear_interpreter_session import clear_interpreter_session

from ..model.init_llms_session import init_llms_session
from ..database.init_database_session import init_database_session
from ..database.init_context_session import init_context_session
from ..interpreter.init_interpreter_session import init_interpreter_session

def display_settings_tab():
    apply = st.button(
        label="Apply settings",
        help="Reset your session to apply your new settings")
    if apply:
        clear_context_session()
        clear_llms_session()
        clear_database_session()
        clear_interpreter_session()
        init_context_session()
        init_llms_session()
        init_database_session()
        init_interpreter_session()
    # Private mode toggle
    with st.expander("**LLM provider settings**"):
        st.session_state.config.private_mode = st.toggle(
            label="Use Private Mode",
            help="Use Text Generation endpoint instead of OpenAI",
        )
        # OpenAI API key
        st.write("**TogetherAI settings**")
        if "TOGETHER_API_KEY" in os.environ:
            llm_provider_api_key = os.environ["TOGETHER_API_KEY"]
        else:
            llm_provider_api_key = "your-api-key"
        os.environ["TOGETHER_API_KEY"] = st.text_input(
            label="TogetherAI API key",
            help="The TogetherAI API key",
            type="password",
            value=llm_provider_api_key)

        st.session_state.config.embeddings_model = st.text_input(
            label="Text Embedding Model",
            value=st.session_state.config.embeddings_model
        )

        st.session_state.config.dim = st.slider(
            "Embedding Dimension",
            min_value=0,
            max_value=3000,
            value=st.session_state.config.embeddings_dim,
        )

        st.session_state.config.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.config.temperature,
        )

        st.session_state.config.top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.config.top_p,
        )
        st.session_state.config.top_k = st.slider(
            "Top K",
            min_value=1,
            max_value=200,
            value=st.session_state.config.top_k,
        )

        st.session_state.config.repetition_penalty = st.slider(
            "Repetition Penalty",
            min_value=0.0,
            max_value=5.0,
            value=st.session_state.config.repetition_penalty,
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