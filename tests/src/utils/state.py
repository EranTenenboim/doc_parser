from typing import List
from typing import TypedDict
from langchain.schema import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    next: str
    excel_path: str
    documents_processed: bool
    vector_store_updated: bool
    analysis_complete: bool