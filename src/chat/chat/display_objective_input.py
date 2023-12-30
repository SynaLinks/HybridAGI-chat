import streamlit as st

def display_objective_input():
    with st.form('input_form'):
        objective = st.text_area('Please, enter the objective (ensure that the programs have been loaded):')
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.session_state.messages.append({"role": "user", "content": objective})
            try:
                st.session_state.interpreter.start(objective)
            except Exception as e:
                st.warning(e)
