import streamlit as st

def init_llms_session():
    cfg = st.session_state.config
    if st.session_state.config.private_mode:
        from langchain.embeddings import GPT4AllEmbeddings
        from langchain.llms import HuggingFaceTextGenInference

        if "embeddings" not in st.session_state.keys():
            st.session_state.embeddings = GPT4AllEmbeddings()
            st.session_state.embeddings_dim = 384
        
        if "smart_llm" not in st.session_state.keys():
            st.session_state.smart_llm = HuggingFaceTextGenInference(
                    inference_server_url=cfg.local_smart_llm_model_url,
                    max_new_tokens=1024,
                    top_k=10,
                    top_p=0.95,
                    typical_p=0.95,
                    temperature=0.01,
                    repetition_penalty=1.03)
        if "fast_llm" not in st.session_state.keys():
            st.session_state.fast_llm = HuggingFaceTextGenInference(
                    inference_server_url=cfg.local_fast_llm_model_url,
                    max_new_tokens=1024,
                    top_k=10,
                    top_p=0.95,
                    typical_p=0.95,
                    temperature=0.01,
                    repetition_penalty=1.03)
    else:
        from langchain.chat_models import ChatOpenAI
        from langchain.embeddings import OpenAIEmbeddings

        if "embeddings" not in st.session_state.keys():
            st.session_state.embeddings = OpenAIEmbeddings(
                openai_api_key = cfg.openai_api_key)
            st.session_state.embeddings_dim = 1536

        if "smart_llm" not in st.session_state.keys():
            st.session_state.smart_llm = ChatOpenAI(
                temperature = cfg.temperature,
                model_name = cfg.smart_llm_model,
                openai_api_key = cfg.openai_api_key)

        if "fast_llm" not in st.session_state.keys():
            st.session_state.fast_llm = ChatOpenAI(
                temperature = cfg.temperature,
                model_name = cfg.fast_llm_model,
                openai_api_key = cfg.openai_api_key)
