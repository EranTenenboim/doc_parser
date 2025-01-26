from typing import Dict, List, Tuple, TypedDict, Callable
from utils.state import AgentState
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from agents.document_processor import DocumentProcessor
from agents.vector_store import VectorStore
from agents.insurance_analysis import InsuranceAnalysisAgent
from agents.document_store import DocumentStore  
from route import Route

class Supervisor:
    def __init__(self):
        self.agents = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """
        Initialize available agents.
        """
        agent_classes = {
            Route.DOCUMENT_PROCESSOR: DocumentProcessor,
            Route.VECTOR_STORE: VectorStore,
            Route.INSURANCE_ANALYSIS: InsuranceAnalysisAgent,
            Route.DOCUMENT_STORE: DocumentStore  
        }

        for agent_name, agent_class in agent_classes.items():
            pass
            # Existing initialization code...

    

    def create_graph(self) -> StateGraph:
        """
        Create the StateGraph for the agent workflow.
        """
        workflow = StateGraph(AgentState)

        # Define the nodes for available agents
        for agent_name, agent in self.agents.items():
            workflow.add_node(agent_name, agent.run)

        # Define the edges (all agents report back to the router)
        for agent_name in self.agents.keys():
            workflow.add_edge(agent_name, Route.route)

        # Set the entry point
        workflow.set_entry_point(Route.route)

        return workflow

    @staticmethod
    def get_initial_state(excel_path: str, query: str) -> AgentState:
        """
        Create the initial state for the agent workflow.
        """
        return AgentState(
            messages=[HumanMessage(content=query)] if query else [],
            excel_path=excel_path,
            documents_processed=False,
            vector_store_updated=False,
            analysis_complete=False
        )

    def run_workflow(self, excel_path: str, query: str) -> AgentState:
        """
        Run the entire workflow.
        """
        initial_state = self.get_initial_state(excel_path, query)
        graph = self.create_graph()
        final_state = graph.run(initial_state)
        return final_state

    def check_agents(self) -> Dict[str, bool]:
        """
        Check if all required agents are properly initialized and functioning.
        """
        agent_status = {}
        for agent_name in Route.get_agent_order():
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                try:
                    if hasattr(agent, 'run') and callable(getattr(agent, 'run')):
                        agent_status[agent_name] = True
                    else:
                        agent_status[agent_name] = False
                except Exception:
                    agent_status[agent_name] = False
            else:
                agent_status[agent_name] = False
        return agent_status