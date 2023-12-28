import streamlit as st
from .clear_messages import clear_messages

ALLOWED_FILES_EXTENSIONS = [
    "txt",
    "py",
    "js",
    "html",
    "css",
    "cypher",
    "md",
    "json",
    "yaml",
    "yml",
]

def display_objective_input():
    upload_file = st.toggle(
        label="Additional files",
        help="Load additional files into memory")
    submitted = None
    with st.form('input_form'):
        if upload_file:
            uploaded_files = st.file_uploader(
                "Choose the files to upload (only support textual data):",
                accept_multiple_files=True,
                type=ALLOWED_FILES_EXTENSIONS)
            if uploaded_files:
                note = "The user uploaded the following files:"
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    filename = "/home/user/Downloads/"+uploaded_file.name
                    st.session_state.filesystem.add_documents(
                        [filename],
                        [bytes_data])
                    note += "- {filename}"
                if uploaded_files:
                    st.session_state.interpreter.tools_map["UpdateNote"].run(note)
        objective = st.text_area('Please, enter the objective, be as specific as possible (ensure that the programs have been loaded):')
        submitted = st.form_submit_button('Submit')

    if submitted:
        st.session_state.messages.append({"role": "user", "content": objective})
        try:
            st.session_state.interpreter.start(objective)
        except Exception as e:
            st.warning(e)
            clear_messages()
