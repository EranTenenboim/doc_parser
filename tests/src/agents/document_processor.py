from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
import os

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def load_excel(self, file_path: str) -> List[Document]:
        """
        Load Excel file using UnstructuredExcelLoader

        Args:
            file_path: Path to the Excel file

        Returns:
            List of Document objects
        """
        logger.info(f"Loading Excel file: {file_path}")
        loader = UnstructuredExcelLoader(file_path)
        return loader.load()

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Process documents by splitting and extracting metadata

        Args:
            documents: List of raw documents

        Returns:
            List of processed Document objects
        """
        logger.info(f"Processing {len(documents)} documents")
        processed_docs = []
        for doc in documents:
            splits = self.text_splitter.split_documents([doc])
            for split in splits:
                split.metadata["source"] = os.path.basename(doc.metadata.get("source", ""))
                processed_docs.append(split)
        return processed_docs

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main agent function to be called by the supervisor

        Args:
            state: Current state of the system

        Returns:
            Updated state
        """
        excel_path = state.get("excel_path")
        if not excel_path:
            logger.warning("No Excel file path provided in the state")
            return state

        raw_documents = self.load_excel(excel_path)
        processed_documents = self.process_documents(raw_documents)

        state["documents"] = processed_documents
        state["documents_processed"] = True
        logger.info(f"Processed {len(processed_documents)} documents")
        return state
