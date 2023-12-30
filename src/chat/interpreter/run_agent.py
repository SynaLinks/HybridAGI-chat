import streamlit as st

def run_agent():
    if "stop" not in st.session_state.keys():
        st.session_state.stop = False
    if st.session_state.stop:
        st.session_state.interpreter.stop()
        st.toast("Program stopped by the User!", icon="⚠️")
    else:
        if not st.session_state.interpreter.finished():
            while not st.session_state.interpreter.finished():
                try:
                    st.session_state.interpreter.run_step()
                except Exception as e:
                    st.error(f"Error occured: {e}")
                    st.session_state.interpreter.stop()
            st.toast("Program executed successfully")