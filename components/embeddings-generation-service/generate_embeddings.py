import os
import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict
from common.postgres_db import Session, Article


# Initialize Qdrant client
QDRANT_HOST = "localhost" if os.getenv("ENVIRONMENT") == "local" else "qdrant"
qdrant_client = QdrantClient(host=QDRANT_HOST, port=6333)

# Create collection (run once)
COLLECTION_NAME = "romanian_laws"
EMBEDDING_DIM = 768  # Verify your model's output dimension

try:
    qdrant_client.get_collection(COLLECTION_NAME)
except Exception:
    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=EMBEDDING_DIM,
            distance=models.Distance.COSINE
        )
    )


def store_embeddings_qdrant(article: Article, embeddings: List, chunks: List[str]):
    """Store embeddings in Qdrant with article metadata"""
    points = []
    
    for idx, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
        points.append(
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "article_id": article.id,
                    "source": article.source,
                    "law_id": article.article_id,
                    "chunk_index": idx,
                    "chunk_text": chunk,
                    "title": article.article_title,
                    "section": article.section,
                    "chapter": article.chapter
                }
            )
        )
    
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def get_all_articles(source=None):
    """
    Retrieve all articles from the database, optionally filtered by source.
    
    Args:
        source (str, optional): The source to filter by. If None, returns all articles.
    
    Returns:
        List[Article]: A list of Article objects.
    """
    session = Session()
    try:
        if source:
            return session.query(Article).filter_by(source=source).all()
        else:
            return session.query(Article).all()
    finally:
        session.close()


def get_chunks(model, text: str, overlap_ratio=0.25) -> List[str]:
    """Return text chunks for embedding"""
    tokenizer = model.tokenizer
    tokens = tokenizer.encode(text, add_special_tokens=False)
    context_size = model.max_seq_length
    effective_window = context_size - tokenizer.num_special_tokens_to_add()
    overlap = int(effective_window * overlap_ratio)
    step = effective_window - overlap
    
    chunks = []
    for start in range(0, len(tokens), step):
        end = start + effective_window
        chunk_tokens = tokens[start:end]
        chunks.append(tokenizer.decode(chunk_tokens, clean_up_tokenization_spaces=True))
    
    return chunks


def search_laws(query: str, model, top_k=5) -> List[Dict]:
    """Search laws using semantic similarity"""
    # Generate query embedding
    query_embedding = model.encode(query).tolist()
    
    # Search Qdrant
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True
    )
    
    # Get full article details from PostgreSQL
    output = []
    session = Session()
    try:
        for hit in results:
            article = session.query(Article).get(hit.payload["article_id"])
            output.append({
                "score": hit.score,
                "text": hit.payload["chunk_text"],
                "article_title": article.article_title,
                "full_text": article.article_body,
                "reference": f"{article.source}/{article.article_id}"
            })
    finally:
        session.close()
    
    return output


def main():
    print("Fetching all articles...")
    all_articles = get_all_articles()

    print("Loading embedding model...")
    model = SentenceTransformer('BlackKakapo/stsb-xlm-r-multilingual-ro')
    
    for article in all_articles:
        # Generate chunks and embeddings
        chunks = get_chunks(model, article.article_body)  # Modified from get_embeddings
        embeddings = model.encode(chunks)
        
        # Store in Qdrant
        store_embeddings_qdrant(article, embeddings, chunks)
        
        print(f"Stored {len(embeddings)} chunks for article {article.id}")


if __name__ == '__main__':
    main()
