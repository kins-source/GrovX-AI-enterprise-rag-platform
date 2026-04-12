from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import time

from utils.security import get_api_key
from utils.logger import logger
from utils.telemetry import track_latency_async
from rag.document_loader import load_document
from rag.chunking import chunk_documents
from rag.vector_store import add_documents_to_store
from agents.orchestrator import process_query

app = FastAPI(title="Enterprise AI Knowledge Assistant", version="1.0.0")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    latency_seconds: float

@app.post("/upload", dependencies=[Depends(get_api_key)])
@track_latency_async
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint for uploading PDF/TXT documents into the Knowledge Base.
    """
    logger.info(f"Received file upload request: {file.filename}")
    try:
        content = await file.read()
        docs = load_document(content, file.filename)
        chunks = chunk_documents(docs)
        add_documents_to_store(chunks)
        return {"message": f"Successfully processed and stored {file.filename}."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        logger.error(f"Upload error: {e}\n{trace}")
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

@app.post("/query", response_model=QueryResponse, dependencies=[Depends(get_api_key)])
@track_latency_async
async def query_assistant(request: QueryRequest):
    """
    Endpoint for querying the agentic assistant.
    """
    start_time = time.time()
    try:
        result = process_query(request.query)
        latency = round(time.time() - start_time, 4)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            latency_seconds=latency
        )
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail="System encountered an error processing query.")

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
