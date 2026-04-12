import os
from tempfile import NamedTemporaryFile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from utils.logger import logger

def load_document(file_content: bytes, filename: str):
    """
    Loads a document from bytes into Langchain Documents.
    Supports PDF and TXT.
    """
    ext = os.path.splitext(filename)[1].lower()
    
    with NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        temp_file.write(file_content)
        temp_path = temp_file.name

    try:
        if ext == ".pdf":
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
        elif ext == ".txt":
            # Using UnstructuredFileLoader instead to gracefully handle encoding issues
            from langchain_community.document_loaders import UnstructuredFileLoader
            loader = UnstructuredFileLoader(temp_path)
            docs = loader.load()
        else:
            from langchain_community.document_loaders import UnstructuredFileLoader
            loader = UnstructuredFileLoader(temp_path)
            docs = loader.load()
        
        # Add source metadata
        for doc in docs:
            doc.metadata["source"] = filename
            
        logger.info(f"Loaded {len(docs)} pages/sections from {filename}")
        return docs
    finally:
        os.remove(temp_path)
