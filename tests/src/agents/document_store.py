from typing import Dict, Any, List
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)
class DocumentStore:
    def __init__(self):
        self.documents = {}  # Simple in-memory storage for demonstration

    def store_document(self, document: Document):
        """
        Store a document in the document store

        Args:
            document: Document object to store
        """
        doc_id = document.metadata.get('source', str(len(self.documents)))
        self.documents[doc_id] = document
        logger.info(f"Stored document with ID: {doc_id}")

    def retrieve_document(self, document_id: str) -> Document:
        """
        Retrieve a document from the document store

        Args:
            document_id: ID of the document to retrieve

        Returns:
            Retrieved Document object
        """
        document = self.documents.get(document_id)
        if document:
            logger.info(f"Retrieved document with ID: {document_id}")
            return document
        else:
            logger.warning(f"Document with ID {document_id} not found")
            return None
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main function to be called by the supervisor

        Args:
            state: Current state of the system

        Returns:
            Updated state
        """
        if 'documents' in state and state.get('store_documents', False):
            for doc in state['documents']:
                self.store_document(doc)
            state['documents_stored'] = True
            logger.info(f"Stored {len(state['documents'])} documents")

        if state.get('retrieve_documents', False):
            retrieved_docs = []
            for doc_id in state.get('document_ids', []):
                doc = self.retrieve_document(doc_id)
                if doc:
                    retrieved_docs.append(doc)
            state['retrieved_documents'] = retrieved_docs
            logger.info(f"Retrieved {len(retrieved_docs)} documents")

        return state

    def get_all_documents(self) -> List[Document]:
        """
        Retrieve all documents from the document store

        Returns:
            List of all stored Document objects
        """
        return list(self.documents.values())