import streamlit as st
from .ui.init_config import init_config
from .ui.init_chat_messages import init_chat_messages
from .ui.init_llms_session import init_llms_session
from .ui.init_database_session import init_database_session
from .ui.init_interpreter_session import init_interpreter_session

from .ui.display_objective_input import display_objective_input
from .ui.display_answer_input import display_answer_input

from .ui.display_chat_messages import display_chat_messages
from .ui.display_settings import display_settings

from .ui.run_agent import run_agent

def initialize() -> bool:
    init_chat_messages()
    init_llms_session()
    success = init_database_session()
    if success:
        init_interpreter_session()
        return True
    return False

def main():
    st.set_page_config(
        "Chat - HybridAGI",
        page_icon = "img/favicon.ico",
        layout = "wide",
    )

    init_config()
    st.write("![Beta](https://img.shields.io/badge/Release-Beta-blue)\
 [![Docs](https://img.shields.io/badge/HybridAGI-Documentation-green)](https://synalinks.github.io/documentation/)\
 [![Docs](https://img.shields.io/badge/Database-Inspection-red)](http://localhost:8001)")
    cfg = st.session_state.config

    tab1, tab2 = st.tabs(["Chat", "Settings"])

    display_answer_input()

    with tab1:
        initialized = initialize()
        if initialized:
            display_objective_input()
            display_chat_messages()
            run_agent()
        else:
            st.error("Please, update your settings and apply the changes before starting")
    with tab2:
        display_settings()

