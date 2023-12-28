import streamlit as st

def display_database_panel():
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
                    folders=[cfg.documentation_directory],
                    folder_names=["/home/user/Documentation"])
    
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