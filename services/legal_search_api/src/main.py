from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, AsyncGenerator
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import asyncio
from core.qdrant_db import search_laws

# Configuration
EMBEDDING_MODEL = "BlackKakapo/stsb-xlm-r-multilingual-ro"
LLM_MODEL = "teapotai/teapotllm"

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Load models during startup
    app.state.embedder = SentenceTransformer(EMBEDDING_MODEL)
    app.state.generator = pipeline(
        "text2text-generation",
        LLM_MODEL
    )
    print(f"Loaded models: {EMBEDDING_MODEL} and {LLM_MODEL}")
    yield

app = FastAPI(
    title="Legal QA System",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

class LawResult(BaseModel):
    score: float
    text: str
    article_title: str
    full_text: str
    reference: str

class QAResponse(BaseModel):
    answer: str
    context: List[LawResult]

def format_prompt(question: str, laws: List[LawResult]) -> str:
    context = "\n\n".join(
        f"Legea ({law["reference"]}):\n{law["text"]}\n\n"
        for law in laws
    )
    return f"""Răspunde la întrebarea juridică folosind exclusiv informațiile din textele de lege oferite. 
            Dacă informațiile sunt insuficiente, răspunde că nu poți oferi un răspuns sigur bazat pe legislația actuală.

            ÎNTREBARE: {question}

            TEXTE LEGALE RELEVANTE:
            {context}

            RĂSPUNS:"""

@app.post("/ask", response_model=QAResponse)
async def generate_answer(request: Request, query: QueryRequest):
    # Retrieve relevant laws
    laws = search_laws(
        query.question,
        request.app.state.embedder,
        query.top_k
    )
    
    # Generate LLM prompt
    prompt = format_prompt(query.question, laws)

    print("Asking LLM...")
    
    # Run LLM generation in thread pool
    answer = app.state.generator(prompt)
    
    return QAResponse(
        answer=answer,
        context=laws
    )

@app.post("/query", response_model=List[LawResult])
async def query_laws(request: Request, query_request: QueryRequest):
    """Original semantic search endpoint"""
    results = search_laws(
        query_request.question,
        request.app.state.embedder,
        query_request.top_k
    )
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
