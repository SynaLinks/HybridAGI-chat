import streamlit as st
from .display_chat_messages import display_chat_messages
from .clear_messages import clear_messages
from ..interpreter.run_agent import run_agent
from .display_objective_input import display_objective_input

def display_chat_tab():
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔁 Reset Chat"):
            st.session_state.interpreter.stop()
            clear_messages()

    pause = False
    with col2:
        pause = st.toggle("⏯️ Pause/Resume")

    with col3:
        if st.button("🛑 Stop"):
            st.session_state.interpreter.stop()
    
    display_objective_input()
    with st.empty().container():
        display_chat_messages()
        if not pause:
            run_agent()