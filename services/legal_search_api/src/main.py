from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, AsyncGenerator
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from core.qdrant_db import search_laws
from openai import OpenAI
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
EMBEDDING_MODEL = "BlackKakapo/stsb-xlm-r-multilingual-ro"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Load models during startup
    app.state.embedder = SentenceTransformer(EMBEDDING_MODEL)
    app.state.generator = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    print(f"Loaded embeded model: {EMBEDDING_MODEL}")
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
    link: str
    reference: str

class QAResponse(BaseModel):
    answer: str
    context: List[LawResult]

def format_prompt(question: str, laws: List[LawResult]) -> List[dict]:
    context = "\n\n".join(
        f"Legea {law['reference']}:\nLink: {law['link']}\n{law['text']}\n\n"
        for law in laws
    )
    
    return [
        {
            "role": "system",
            "content": "Răspunde la întrebarea juridică folosind exclusiv informațiile din textele de lege oferite. " + \
            "Dacă informațiile sunt insuficiente, răspunde că nu poți oferi un răspuns sigur bazat pe legislația actuală." + \
            "În răspunsul tău, include link-uri către textele de lege relevante pentru a permite utilizatorului să verifice informațiile. " + \
            "Răspunsul tău trebuie să fie concis și la obiect. "
        },
        {
            "role": "user",
            "content": f"ÎNTREBARE: {question}\n\nTEXTE LEGALE RELEVANTE:\n{context}\n\nRĂSPUNS:"
        }
    ]


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
    answer = app.state.generator.chat.completions.create(
        model="deepseek-chat",
        messages=prompt,
        stream=False
    )
    
    return QAResponse(
        answer=answer.choices[0].message.content,
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
