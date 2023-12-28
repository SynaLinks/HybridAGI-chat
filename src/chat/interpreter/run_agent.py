import streamlit as st
from ..chat.clear_messages import clear_messages

def run_agent():
    if "stop" not in st.session_state.keys():
        st.session_state.stop = False
    if st.session_state.stop:
        st.session_state.interpreter.stop()
        clear_messages()
        st.toast("Program stopped by the User!", icon="⚠️")
    else:
        if not st.session_state.interpreter.finished():
            while not st.session_state.interpreter.finished():
                try:
                    st.session_state.interpreter.run_step()
                except Exception as e:
                    st.toast(f"Error occured: {e}")
                    st.session_state.interpreter.stop()
                    st.stop()
            clear_messages()
            st.toast("Program executed successfully")
            
            
