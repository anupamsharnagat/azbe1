from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag_backend.api.routes import router

app = FastAPI(
    title="Azure LangChain RAG API",
    description="API for parsing PDFs containing tables/text and querying via Azure OpenAI.",
    version="1.0.0"
)

# Enable CORS for the frontend application
# I am allowing all origins ('*') for local  but in production i will give specific, 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register our RAG specific routes
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    """
    Health check root API point.
    """
    return {"message": "Welcome to the Azure LangChain RAG API"}
