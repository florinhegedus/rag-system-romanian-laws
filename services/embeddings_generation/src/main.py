from sentence_transformers import SentenceTransformer
from typing import List
from core.postgres_db import Session, Article
from core.qdrant_db import setup_qdrant_collection, store_embeddings_qdrant


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
        # if the chunk is too small and it is contained in the previous chunk, break
        if start != 0 and len(chunk_tokens) < overlap:
            break
        chunks.append(tokenizer.decode(chunk_tokens, clean_up_tokenization_spaces=True))
    
    return chunks


def main():
    print("Fetching all articles...")
    all_articles = get_all_articles()

    print("Loading embedding model...")
    model = SentenceTransformer('BlackKakapo/stsb-xlm-r-multilingual-ro')

    setup_qdrant_collection()
    
    for article in all_articles:
        # Generate chunks and embeddings
        chunks = get_chunks(model, article.article_body)  # Modified from get_embeddings
        embeddings = model.encode(chunks)
        
        # Store in Qdrant
        store_embeddings_qdrant(article, embeddings, chunks)


if __name__ == '__main__':
    main()
