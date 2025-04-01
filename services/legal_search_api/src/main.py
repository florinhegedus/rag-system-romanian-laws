from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
from core.qdrant_db import search_laws

# Initialize FastAPI app
app = FastAPI(title="Legal Semantic Search API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model (ensure this matches what was used for embeddings)
MODEL_NAME = "BlackKakapo/stsb-xlm-r-multilingual-ro"  # Update with your model
model = None

@app.on_event("startup")
async def load_embedding_model():
    global model
    model = SentenceTransformer(MODEL_NAME)
    print(f"Loaded embedding model: {MODEL_NAME}")

# Request/Response models
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
async def query_laws(request: QueryRequest):
    """
    Endpoint to search relevant laws based on a natural language question
    
    Parameters:
    - question: The legal question to analyze
    - top_k: Number of most relevant results to return (default:5)
    """
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    results = search_laws(request.question, model, request.top_k)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
