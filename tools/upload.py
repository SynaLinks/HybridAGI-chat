from typing import Optional
import streamlit as st
from hybridagi.tools import UploadTool
from langchain.callbacks.manager import CallbackManagerForToolRun

class StreamlitUploadTool(UploadTool):
    def _run(
            self,
            query:str,
            run_manager: Optional[CallbackManagerForToolRun] = None
        ) -> str:
        """Upload and display a toast"""
        result = super().upload(query)
        st.toast(f"{result}", icon="🎉")
        return result