# main.py (updated)
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, AsyncGenerator
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from core.qdrant_db import search_laws


# Load embedding model early to catch errors
MODEL_NAME = "BlackKakapo/stsb-xlm-r-multilingual-ro"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup code
    app.state.model = SentenceTransformer(MODEL_NAME)
    print(f"Loaded embedding model: {MODEL_NAME}")
    yield
    # Shutdown code (optional)
    # If you need to clean up resources
    

# Initialize FastAPI with lifespan
app = FastAPI(
    title="Legal Semantic Search API",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models remain the same
class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class LawResult(BaseModel):
    score: float
    text: str
    article_title: str
    full_text: str
    reference: str


@app.post("/query", response_model=List[LawResult])
async def query_laws(request: Request, query_request: QueryRequest):
    """
    Endpoint to search relevant laws based on a natural language question
    
    Parameters:
    - question: The legal question to analyze
    - top_k: Number of most relevant results to return (default:5)
    """
    model = request.app.state.model
    results = search_laws(query_request.question, model, query_request.top_k)
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
