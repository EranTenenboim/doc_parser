from typing import Dict, List, TypedDict
from utils.state import AgentState
from langgraph.graph import END

class AgentOutput(TypedDict):
    next: List[str]
    state: AgentState

from enum import Enum

class Route(Enum):
    DOCUMENT_PROCESSOR = "document_processor"
    VECTOR_STORE = "vector_store"
    INSURANCE_ANALYSIS = "insurance_analysis"
    DOCUMENT_STORE = "document_store" 

    # Constants for state keys
    DOCUMENTS_PROCESSED = "documents_processed"
    VECTOR_STORE_UPDATED = "vector_store_updated"
    ANALYSIS_COMPLETE = "analysis_complete"

    @staticmethod
    def route(state: AgentState) -> AgentOutput:
        """
        Route the workflow based on the current state.
        """
        if not state[Route.DOCUMENTS_PROCESSED]:
            return AgentOutput(next=[Route.DOCUMENT_PROCESSOR], state=state)
        elif not state[Route.VECTOR_STORE_UPDATED]:
            return AgentOutput(next=[Route.VECTOR_STORE], state=state)
        elif not state[Route.ANALYSIS_COMPLETE]:
            return AgentOutput(next=[Route.INSURANCE_ANALYSIS], state=state)
        else:
            return AgentOutput(next=[END], state=state)

    @staticmethod
    def get_agent_order() -> List[str]:
        """
        Return the order of agents in the workflow.
        """
        return [
            Route.DOCUMENT_PROCESSOR,
            Route.VECTOR_STORE,
            Route.INSURANCE_ANALYSIS
        ]