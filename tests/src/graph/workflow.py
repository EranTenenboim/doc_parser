from langgraph.graph import StateGraph
from agents.document_processor import DocumentProcessor
from agents.vector_store import VectorStore
from agents.insurance_analysis import InsuranceAnalysisAgent
from supervisor import Supervisor
from agents.document_store import DocumentStore

def create_agent_graph(
    doc_processor: DocumentProcessor,
    vector_store: VectorStore,
    analysis_agent: InsuranceAnalysisAgent,
    document_store: DocumentStore
) -> StateGraph:
    """
    Creates the agent workflow graph.

    Args:
        doc_processor: DocumentProcessor instance
        vector_store: VectorStore instance
        analysis_agent: InsuranceAnalysisAgent instance
        document_store: DocumentStore instance

    Returns:
        Compiled workflow graph
    """
    agents = {
        Supervisor.DOCUMENT_PROCESSOR: doc_processor.run,
        Supervisor.VECTOR_STORE: vector_store.run,
        Supervisor.INSURANCE_ANALYSIS: analysis_agent.run,
        Supervisor.DOCUMENT_STORE: document_store.run, 
    }

    workflow = Supervisor.create_graph(agents)

    return workflow.compile()