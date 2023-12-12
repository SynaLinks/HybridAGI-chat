"""The speak tool. Copyright (C) 2023 SynaLinks. License: GPL-3.0"""

import streamlit as st
from colorama import Fore
from colorama import Style
from typing import Optional
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.tools import BaseTool, StructuredTool, Tool, tool

class SpeakTool(BaseTool):
    name = "Speak"
    description = \
    """
    Usefull to tell information to the User.
    """
    def _run(
            self,
            query:str,
            run_manager: Optional[CallbackManagerForToolRun] = None
        ) -> str:
        """Use the tool."""
        query = query.strip('"')
        st.session_state.messages.append({"role": "assistant", "content": query})
        with st.chat_message("assistant"):
            st.write(query)
        return "Success"

    async def _arun(self, query: str,  run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Speak does not support async")