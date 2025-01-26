import pytest
from unittest.mock import patch
from src.agents.document_processor import DocumentProcessor
from langchain_core.documents import Document

@pytest.fixture
def document_processor():
    return DocumentProcessor()

def test_run_with_excel_path(document_processor):
    with patch.object(DocumentProcessor, 'load_excel') as mock_load_excel, \
         patch.object(DocumentProcessor, 'process_documents') as mock_process_documents:

        mock_load_excel.return_value = [Document(page_content="Test content")]
        mock_process_documents.return_value = [Document(page_content="Processed content")]

        initial_state = {"excel_path": "test.xlsx"}
        result_state = document_processor.run(initial_state)

        assert result_state["documents_processed"] is True
        assert len(result_state["documents"]) == 1
        assert result_state["documents"][0].page_content == "Processed content"

# Rest of the file remains the same

def test_run_no_excel_path(document_processor):
    initial_state = {}
    result_state = document_processor.run(initial_state)

    assert "documents" not in result_state
    assert "documents_processed" not in result_state

def test_process_documents(document_processor):
    input_docs = [
        Document(page_content="Test content 1", metadata={"source": "file1.xlsx"}),
        Document(page_content="Test content 2", metadata={"source": "file2.xlsx"})
    ]

    result = document_processor.process_documents(input_docs)

    assert len(result) > 0
    for doc in result:
        assert isinstance(doc, Document)
        assert "source" in doc.metadata
        assert doc.metadata["source"] in ["file1.xlsx", "file2.xlsx"]