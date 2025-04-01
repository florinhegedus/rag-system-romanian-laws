import os
from uuid import uuid5, NAMESPACE_DNS
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict
from core.postgres_db import Session, Article


# Initialize Qdrant client
QDRANT_HOST = "localhost" if os.getenv("ENVIRONMENT") == "local" else "qdrant"
qdrant_client = QdrantClient(host=QDRANT_HOST, port=6333)

# Create collection (run once)
COLLECTION_NAME = "romanian_laws"
EMBEDDING_DIM = 768  # Verify your model's output dimension


def setup_qdrant_collection():
    try:
        qdrant_client.get_collection(COLLECTION_NAME)
        # Only reaches here if collection exists
        if os.getenv("RESET_EMBEDDINGS") == "true":
            print("Collection exists, starting deletion...")
            qdrant_client.delete_collection(COLLECTION_NAME)
            raise ValueError("Forcing recreation")
        else:
            print("Collection already exists, skipping creation.")
    except (ValueError, Exception):  # Explicitly catch Qdrant's not found error
        print("Collection does not exist, creating...")
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=EMBEDDING_DIM,
                distance=models.Distance.COSINE
            )
        )


def store_embeddings_qdrant(article: Article, embeddings: List, chunks: List[str]):
    """ Store embeddings in Qdrant with article metadata. If the article already exists, it will be overwritten. """
    points = []
    
    for idx, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
        # Generate deterministic UUID from article ID and chunk index
        point_id = str(uuid5(NAMESPACE_DNS, f"{article.id}_{idx}"))

        points.append(
            models.PointStruct(
                id=point_id,
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
    print(f"Stored {len(embeddings)} chunks for article {article.id}")


def check_existence_and_store_embeddings_qdrant(article: Article, embeddings: List, chunks: List[str]):
    """Store embeddings only if not already present in Qdrant"""
    points = []
    for idx, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
        point_id = str(uuid5(NAMESPACE_DNS, f"{article.id}_{idx}"))
        
        # Skip if already exists
        existing = qdrant_client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[point_id]
        )

        if existing:
            print(f"Point {point_id} already exists in Qdrant.")
        else:
            # If not, store it
            print(f"Point {point_id} does not exist, storing...")
            points.append(
                models.PointStruct(
                    id=point_id,
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
    if len(points) > 0:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print(f"Stored {len(embeddings)} chunks for article {article.id}")


def search_laws(query: str, model, top_k=5) -> List[Dict]:
    """Search laws using semantic similarity"""
    # Generate query embedding
    query_embedding = model.encode(query).tolist()
    
    # Search Qdrant
    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        with_payload=True
    )
    
    # Get full article details from PostgreSQL
    output = []
    session = Session()
    try:
        for hit in results.points:
            article = session.get(Article, hit.payload["article_id"])
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
