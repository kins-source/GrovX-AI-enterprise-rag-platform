from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger import logger

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Splits Langchain Documents into manageable chunks to fit context windows.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks
