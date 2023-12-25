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
    cfg = st.session_state.config
    col1, col2, col3 = st.columns(3)

    with col1:
        clear_database = st.button(
            label='Clear database',
            help="Clear the hybrid vector/graph database")
        if clear_database:
            st.session_state.program_memory.clear()
            st.session_state.filesystem.clear()
            st.session_state.program_memory.initialize()
            st.session_state.filesystem.initialize()

    with col2:
        load_documentation = st.button(
            label='Load documentation',
            help="Load the folder containing your documentation")
        if load_documentation:
            with st.spinner("This may take a while..."):
                st.session_state.filesystem.add_folders(
                    folders=[cfg.downloads_directory],
                    folder_names=["/home/user/Downloads/documentation"])
    
    with col3:
        load_programs = st.button(
            label='Load programs',
            help="Load the Cypher programs into memory")
        if load_programs:
            try:
                with st.spinner("This may take a while..."):
                    st.session_state.program_memory.load_folders(cfg.library_directory)
            except Exception as err:
                st.warning(f"Error occured while loading cypher programs: {str(err)}", icon='⚠')
    
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
