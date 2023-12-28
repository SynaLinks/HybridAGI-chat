"""The ask user tool. Copyright (C) 2023 SynaLinks. License: GPL-3.0"""

import streamlit as st
from typing import Optional
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.tools import BaseTool
class AskUserTool(BaseTool):
    name = "AskUser"
    description = \
    """
    Usefull to ask User for additionnal information.
    The Observation is from the perspective of the User responding to you.
    """
    def _run(
            self,
            query:str,
            run_manager: Optional[CallbackManagerForToolRun] = None
        ) -> str:
        """Use the tool."""
        answer = ""
        if st.session_state.answer:
            answer = st.session_state.answer
            st.session_state.answer = ""
        else:
            st.session_state.messages.append({"role": "assistant", "content": query})
            st.session_state.request_answer = True
            with st.chat_message("assistant", avatar="src/img/logo.png"):
                st.write(query)
            st.stop()
        return "User answer: " + answer

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("AskUser does not support async")

