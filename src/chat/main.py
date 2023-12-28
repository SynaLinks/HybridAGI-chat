import streamlit as st
from .settings.init_config import init_config

from .settings.display_settings_tab import display_settings_tab

from .chat.display_answer_input import display_answer_input
from .chat.display_chat_tab import display_chat_tab

from .database.display_database_panel import display_database_panel
from .database.init_database_session import init_database_session
from .database.init_context_session import init_context_session
from .model.init_llms_session import init_llms_session
from .interpreter.init_interpreter_session import init_interpreter_session

def main():
    st.set_page_config(
        page_title = "Chat - HybridAGI",
        page_icon = "src/img/favicon.ico",
        layout = "wide",
    )

    st.write("![Beta](https://img.shields.io/badge/Release-Beta-blue)\
 [![Docs](https://img.shields.io/badge/HybridAGI-Documentation-green)](https://synalinks.github.io/documentation/)\
 [![Docs](https://img.shields.io/badge/Database-Inspection-red)](http://localhost:8001)")

    init_config()
    init_context_session()
    init_llms_session()
    init_database_session()
    init_interpreter_session()

    display_database_panel()

    tab1, tab2 = st.tabs(["Chat", "Settings"])
    with tab1:
        display_chat_tab()

    with tab2:
        display_settings_tab()

    display_answer_input()