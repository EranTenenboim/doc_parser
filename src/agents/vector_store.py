from typing import Dict, Any, List
from langchain_core.documents import Document
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import OpenAIEmbeddings
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.connection_string = self._get_neon_connection_string()
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = self._initialize_vector_store()

    def _get_neon_connection_string(self) -> str:
        """Construct the Neon connection string from environment variables."""
        db_host = os.getenv("NEON_DB_HOST")
        db_name = os.getenv("NEON_DB_NAME")
        db_user = os.getenv("NEON_DB_USER")
        db_password = os.getenv("NEON_DB_PASSWORD")

        if not all([db_host, db_name, db_user, db_password]):
            raise ValueError("Missing Neon database credentials in environment variables")

        return f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

    def _initialize_vector_store(self) -> PGVector:
        """Initialize the PGVector store with Neon database."""
        return PGVector.from_documents(
            documents=[],  # Start with an empty collection
            embedding=self.embeddings,
            collection_name="insurance_docs",
            connection_string=self.connection_string,
        )

    def add_documents(self, documents: List[Document]):
        logger.info(f"Adding {len(documents)} documents to vector store")
        self.vector_store.add_documents(documents)

    def search(self, query: str, k: int = 5) -> List[Document]:
        logger.info(f"Searching for query: {query}")
        return self.vector_store.similarity_search(query, k=k)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if state.get("documents_processed") and "documents" in state:
            self.add_documents(state["documents"])
            state["documents_vectorized"] = True
            logger.info("Documents added to vector store")

        if state.get("perform_search") and "query" in state:
            results = self.search(state["query"])
            state["search_results"] = results
            logger.info(f"Search completed, found {len(results)} relevant documents")

        return state
