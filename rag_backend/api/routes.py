from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil

from rag_backend.services.document_parser import extract_text_and_tables_from_pdf
from rag_backend.services.rag_service import create_and_save_vector_store, answer_query

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Synchronous upload and processing.
    The request waits until the vector store is ready.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    
    try:
        # Step 1: Parse (PyMuPDF)
        documents = extract_text_and_tables_from_pdf(file_path)
        
        # Step 2: Index (FAISS)
        total_chunks = create_and_save_vector_store(documents)
        
        return {
            "message": "Processed successfully",
            "filename": file.filename,
            "chunks": total_chunks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/ask", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    """Simple RAG retrieval."""
    try:
        answer = answer_query(request.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
