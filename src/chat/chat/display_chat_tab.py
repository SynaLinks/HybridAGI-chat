import streamlit as st
from ..database.init_database_session import init_database_session
from ..interpreter.init_interpreter_session import init_interpreter_session
from ..model.init_llms_session import init_llms_session

from .init_chat_messages import init_chat_messages
from .display_objective_input import display_objective_input
from .display_chat_messages import display_chat_messages

from ..interpreter.run_agent import run_agent

def initialize_chat() -> bool:
    """Initialize the chat tab"""
    init_chat_messages()
    init_llms_session()
    success = init_database_session()
    if success:
        init_interpreter_session()
        return True
    return False

def display_chat_tab():
    initialized = initialize_chat()
    if initialized:
        display_objective_input()
        display_chat_messages()
        run_agent()
    else:
        st.error(
            "Please, update your settings and apply the changes "+
            "before starting to chat with the model"
        )