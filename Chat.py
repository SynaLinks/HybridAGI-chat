import asyncio
import os
import base64
import numpy as np
import streamlit as st
from langchain.tools import Tool
from langchain.tools import DuckDuckGoSearchRun
from typing import List

from hybridagi import FileSystem, FileSystemContext
from hybridagi import ProgramMemory
from hybridagi import TraceMemory

from tools.ask_user import AskUserTool
from tools.speak import SpeakTool

from langchain.tools import DuckDuckGoSearchRun

from hybridagi import GraphProgramInterpreter

from hybridagi.toolkits import (
    FileSystemToolKit,
)

from hybridagi.config import Config

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

def _normalize_vector(value):
    return np.add(np.divide(value, 2), 0.5)

def _pre_action_callback(
        purpose: str,
        tool: str,
        prompt: str):
    st.session_state.action_status = st.status(purpose)
    with st.session_state.action_status:
        st.write(f"**Tool:** `{tool}`")

def _post_action_callback(
        purpose: str,
        tool: str,
        input: str,
        observation: str):
    if "action_status" in st.session_state.keys():
        if st.session_state.action_status:
            with st.session_state.action_status:
                st.write(f"**Input:**\n{input}")
                st.write(f"**Observation:**\n{observation}")
            st.session_state.action_status = None

def _pre_decision_callback(
        purpose: str,
        question: str,
        options: List[str]):
    st.session_state.decision_status = st.status(purpose)
    with st.session_state.decision_status:
        st.write(f"**Question:**\n{question}")

def _post_decision_callback(
        purpose: str,
        question: str,
        options: List[str],
        decision: str):
    if "decision_status" in st.session_state.keys():
        if st.session_state.decision_status:
            with st.session_state.decision_status:
                st.write(f"**Answer:**\n{decision}")
            st.session_state.decision_status = None

def clear_database():
    st.session_state.program_memory.clear()
    st.session_state.filesystem.clear()
    st.session_state.program_memory.initialize()
    st.session_state.filesystem.initialize()

def init_chat_messages():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = []
    if "answer" not in st.session_state.keys():
        st.session_state.answer = ""
    if "stop" not in st.session_state.keys():
        st.session_state.stop = False

def clear_messages():
    st.session_state.messages = []
    st.session_state.answer = ""
    st.session_state.request_answer = False

def display_user_answer_input():
    # User-provided prompt
    if response := st.chat_input("Enter your response (use `/stop` if you want to stop the AI at any time)"):
        if "request_answer" not in st.session_state.keys():
            st.session_state.request_answer = False
        if st.session_state.request_answer:
            st.session_state.messages.append({"role": "user", "content": response})
            st.session_state.answer = response
        if response == "/stop":
            st.session_state.stop = True
    
def display_chat_messages():
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def display_starting_input():
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
            help="Load the folder containing your documentation (see introduction tutorial)")
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

def run_agent():
    if "stop" not in st.session_state.keys():
        st.session_state.stop = False
    if st.session_state.stop:
        st.session_state.interpreter.stop()
        clear_messages()
        st.toast("Program stopped by the User!", icon="⚠️")
    else:
        if not st.session_state.interpreter.finished():
            while not st.session_state.interpreter.finished() \
                and st.session_state.answer == "":
                try:
                    st.session_state.interpreter.run_step()
                except Exception as e:
                    st.warning(e)
            clear_messages()

def init_config():
    if "config" not in st.session_state.keys():
        st.session_state.config = Config()

    if st.session_state.config.openai_api_key == "your-openai-api-key" and \
        st.session_state.config.private_mode == False:
        st.warning("Please provide your OpenAI API key or switch to private mode")

def clear_interpreter_session():
    if "clear_interpreter" in st.session_state.keys():
        del st.session_state["clear_interpreter"]

def init_interpreter_session():
    cfg = st.session_state.config

    if "interpreter" not in st.session_state.keys():
        ask_user = AskUserTool()
        speak = SpeakTool()
        internet_search = DuckDuckGoSearchRun()

        toolkits = [
            FileSystemToolKit(
                filesystem = st.session_state.filesystem,
                downloads_directory = cfg.downloads_directory,
            )
        ]

        tools = [
            Tool(
                name=ask_user.name,
                func=ask_user.run,
                description=ask_user.description),
            Tool(
                name=speak.name,
                func=speak.run,
                description=speak.description),
            Tool(
                name="InternetSearch",
                func=internet_search.run,
                description=internet_search.description)
        ]
        interpreter = GraphProgramInterpreter(
            program_memory = st.session_state.program_memory,
            trace_memory = st.session_state.trace_memory,
            smart_llm = st.session_state.smart_llm,
            fast_llm = st.session_state.fast_llm,
            tools = tools,
            toolkits = toolkits,
            smart_llm_max_token = cfg.smart_llm_max_token,
            fast_llm_max_token = cfg.fast_llm_max_token,
            max_decision_attemps = cfg.max_decision_attemps,
            max_evaluation_attemps = cfg.max_evaluation_attemps,
            max_iteration = cfg.max_iteration,
            verbose = cfg.verbose,
            debug = cfg.debug_mode,
            pre_action_callback = _pre_action_callback,
            pre_decision_callback = _pre_decision_callback,
            post_action_callback = _post_action_callback,
            post_decision_callback = _post_decision_callback)
        st.session_state.interpreter = interpreter

def clear_database():
    st.session_state.program_memory.clear()
    st.session_state.filesystem.clear()
    st.session_state.program_memory.initialize()
    st.session_state.filesystem.initialize()

def clear_database_session():
    if "filesystem" in st.session_state.keys():
        del st.session_state["filesystem"]
    if "program_memory" in st.session_state.keys():
        del st.session_state["program_memory"]
    if "trace_memory" in st.session_state.keys():
        del st.session_state["trace_memory"]

def init_database_session():
    cfg = st.session_state.config

    if "filesystem_context" not in st.session_state.keys():
        st.session_state.filesystem_context = FileSystemContext()

    if "filesystem" not in st.session_state.keys():
        st.session_state.filesystem = FileSystem(
            redis_url = cfg.redis_url,
            index_name = cfg.memory_index,
            embeddings = st.session_state.embeddings,
            embeddings_dim = st.session_state.embeddings_dim,
            normalize = _normalize_vector,
            context = st.session_state.filesystem_context)
        st.session_state.filesystem.initialize()

    if "program_memory" not in st.session_state.keys():
        st.session_state.program_memory = ProgramMemory(
            redis_url = cfg.redis_url,
            index_name = cfg.memory_index,
            embeddings = st.session_state.embeddings,
            embeddings_dim = st.session_state.embeddings_dim,
            normalize = _normalize_vector)
        st.session_state.program_memory.initialize()

    if "trace_memory" not in st.session_state.keys():
        st.session_state.trace_memory = TraceMemory(
            redis_url = cfg.redis_url,
            index_name = cfg.memory_index,
            embeddings = st.session_state.embeddings,
            embeddings_dim = st.session_state.embeddings_dim,
            normalize = _normalize_vector)
        st.session_state.trace_memory.initialize()

def clear_llms_session():
    if "embeddings" in st.session_state.keys():
        del st.session_state["embeddings"]
    if "smart_llm" in st.session_state.keys():
        del st.session_state["smart_llm"]
    if "fast_llm" in st.session_state.keys():
        del st.session_state["fast_llm"]

def init_llms_session():
    cfg = st.session_state.config

    if st.session_state.config.private_mode:
        from langchain.embeddings import GPT4AllEmbeddings
        from langchain.llms import HuggingFaceTextGenInference

        if "embeddings" not in st.session_state.keys():
            st.session_state.embeddings = GPT4AllEmbeddings()
            st.session_state.embeddings_dim = 384
        
        if "smart_llm" not in st.session_state.keys():
            st.session_state.smart_llm = HuggingFaceTextGenInference(
                    inference_server_url=cfg.local_smart_llm_model_url,
                    max_new_tokens=1024,
                    top_k=10,
                    top_p=0.95,
                    typical_p=0.95,
                    temperature=0.01,
                    repetition_penalty=1.03)
        if "fast_llm" not in st.session_state.keys():
            st.session_state.fast_llm = HuggingFaceTextGenInference(
                    inference_server_url=cfg.local_fast_llm_model_url,
                    max_new_tokens=1024,
                    top_k=10,
                    top_p=0.95,
                    typical_p=0.95,
                    temperature=0.01,
                    repetition_penalty=1.03)
    else:
        from langchain.chat_models import ChatOpenAI
        from langchain.embeddings import OpenAIEmbeddings

        if "embeddings" not in st.session_state.keys():
            st.session_state.embeddings = OpenAIEmbeddings(
                openai_api_key = cfg.openai_api_key)
            st.session_state.embeddings_dim = 1536

        if "smart_llm" not in st.session_state.keys():
            st.session_state.smart_llm = ChatOpenAI(
                temperature = cfg.temperature,
                model_name = cfg.smart_llm_model,
                openai_api_key = cfg.openai_api_key)

        if "fast_llm" not in st.session_state.keys():
            st.session_state.fast_llm = ChatOpenAI(
                temperature = cfg.temperature,
                model_name = cfg.fast_llm_model,
                openai_api_key = cfg.openai_api_key)

def display_settings():
    save = st.button(
        label="Apply settings",
        help="Reset your session to apply your new settings")
    if save:
        clear_llms_session()
        clear_database_session()
        clear_interpreter_session()

    if "config" not in st.session_state.keys():
        st.session_state.config = Config()
    cfg = st.session_state.config
    # Private mode toggle
    with st.expander("**LLM provider settings**"):
        st.session_state.config.private_mode = st.toggle(
            label="Use Private Mode",
            help="Use Text Generation endpoint instead of OpenAI",
        )
        # OpenAI API key
        st.write("**OpenAI settings**")
        openai_api_key = st.text_input(
            label="OpenAI API key",
            help="Used when private mode is disabled",
            type="password",
            value=st.session_state.config.openai_api_key)
        if openai_api_key:
            st.session_state.config.openai_api_key = openai_api_key
        st.session_state.config.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
        )
        st.session_state.config.smart_llm_model = st.text_input(
            label="Smart LLM model",
            value=st.session_state.config.smart_llm_model)
        st.session_state.config.fast_llm_model = st.text_input(
            label="Fast LLM model",
            value=st.session_state.config.fast_llm_model)

        st.write("**Text Generation settings**")
        # Local model URL
        st.session_state.config.local_smart_llm_model_url = st.text_input(
            label="Local smart LLM model URL",
            help="Used when private mode is enabled",
            value=st.session_state.config.local_smart_llm_model_url)
        st.session_state.config.local_fast_llm_model_url = st.text_input(
            label="Local fast LLM model URL",
            help="Used when private mode is enabled",
            value=st.session_state.config.local_fast_llm_model_url)
    # Redis URL
    with st.expander("**Database settings**"):
        st.session_state.config.redis_url = st.text_input(
            label="Redis URL",
            help="Use the URL of the container running the database",
            value=st.session_state.config.redis_url)
    # HybridAGI settings
    with st.expander("**HybridAGI settings**"):
        st.session_state.config.downloads_directory = st.text_input(
            label="Downloads directory",
            help="This is where the AI upload its work",
            value=st.session_state.config.downloads_directory,
        )
        st.session_state.config.documentation_directory = st.text_input(
            label="Documentation directory",
            help="This is where the AI get its unstructured knowledge",
            value=st.session_state.config.documentation_directory,
        )
        st.session_state.config.library_directory = st.text_input(
            label="Library directory",
            help="This is where the AI get its Cypher programs",
            value=st.session_state.config.library_directory,
        )
        st.session_state.config.chunk_size = st.slider(
            "Chunk size",
            min_value=1000,
            max_value=4000,
            value=1500,
            help="Used to chunk documents into manageable size",
        )

        st.session_state.config.chunk_overlap = st.slider(
            "Chunk overlap",
            min_value=0,
            max_value=1000,
            value=0,
            help="Used to chunk documents into manageable size",
        )
        
        st.session_state.config.max_iteration = st.slider(
            "Max iteration",
            min_value=0,
            max_value=2000,
            value=100,
            help="The maximum iteration per run",
        )

        st.session_state.config.max_decision_attemps = st.slider(
            "Max decision attemps",
            min_value=1,
            max_value=10,
            value=5,
            help="The maximum decision attemps before raising an exception",
        )

        st.session_state.config.max_evaluation_attemps = st.slider(
            "Max evaluation attemps",
            min_value=1,
            max_value=10,
            value=5,
            help="The maximum evaluation attemps before raising an exception",
        )

def init_session():
    init_config()
    init_llms_session()
    init_database_session()
    init_interpreter_session()
    init_chat_messages()

def main():
    st.write("![Beta](https://img.shields.io/badge/Release-Beta-blue)\
 [![Docs](https://img.shields.io/badge/HybridAGI-Documentation-green)](https://synalinks.github.io/documentation/)\
 [![Docs](https://img.shields.io/badge/Database-Inspection-red)](http://localhost:8001)")
    init_session()
    
    tab1, tab2 = st.tabs(["Chat", "Settings"])

    display_user_answer_input()

    with tab2:
        display_settings()

    with tab1:
        display_starting_input()
        display_chat_messages()
        run_agent()

if __name__ == '__main__':
    main()