import argparse
import logging
from graph.workflow import create_agent_graph
from supervisor import Supervisor
from agents.document_processor import DocumentProcessor
from agents.vector_store import VectorStore
from agents.insurance_analysis import InsuranceAnalysisAgent
from agents.document_store import DocumentStore  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Insurance Data Analysis Pipeline')
    parser.add_argument('--excel-path', type=str, required=True, help='Path to Excel file for processing')
    parser.add_argument('--query', type=str, help='Analysis query to run')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create individual agents
    document_store = DocumentStore() 
    vector_store = VectorStore()
    document_processor = DocumentProcessor()
    insurance_analysis = InsuranceAnalysisAgent(vector_store)

    # Create the agent graph
    graph = create_agent_graph(document_processor, vector_store, insurance_analysis, document_store)

    # Initialize the state
    initial_state = Supervisor.get_initial_state(args.excel_path, args.query)

    # Run the graph
    for output in graph.stream(initial_state):
        if "__end__" not in output:
            logger.info(f"Intermediate output: {output}")

    logger.info("Analysis complete!")

if __name__ == "__main__":
    main()