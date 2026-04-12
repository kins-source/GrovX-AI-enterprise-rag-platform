from langchain.tools import tool
from rag.vector_store import retrieve_similar_documents
from utils.logger import logger

@tool
def retrieve_enterprise_documents(query: str) -> str:
    """
    REQUIRED FOR ANY QUERY ABOUT TEXT DOCUMENTS, COMPLIANCE, POLICIES, PDFs, OR GENERAL COMPANY KNOWLEDGE.
    Use this tool to search the Vector Store. 
    DO NOT use this tool for structured data like revenue, sales, or orders (use query_sales_database for that).
    """
    logger.info(f"Retrieving documents for query: {query}")
    try:
        # Uses the metadata-filtered retrieval logic scoped to the latest document
        docs = retrieve_similar_documents(query, k=4)
        if not docs:
            return "No relevant documents found."
        
        results = []
        sources_list = []
        for i, d in enumerate(docs):
            source = d.metadata.get("source", "Unknown")
            source_label = f"{source} (Chunk {i+1})"
            sources_list.append(source_label)
            results.append(f"Source [{source_label}]:\n{d.page_content}\n")
        
        import json
        return json.dumps({
            "context": "\n".join(results),
            "sources": sources_list
        })
    except Exception as e:
        logger.error(f"Retrieval Failed: {e}")
        return f"Error retrieving documents: {e}"
