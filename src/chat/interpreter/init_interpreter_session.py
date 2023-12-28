import streamlit as st
from typing import List
from langchain.tools import Tool
from hybridagi import GraphProgramInterpreter
from hybridagi.toolkits.filesystem_toolkit import FileSystemToolKit

from ..tools.ask_user import AskUserTool
from ..tools.speak import SpeakTool
from langchain.tools import DuckDuckGoSearchRun

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