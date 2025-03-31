from common.postgres_db import Session, Article
from sentence_transformers import SentenceTransformer


def get_embeddings(model, text, overlap_ratio=0.25):
    """
    Generate embeddings with sliding window and overlap
    
    Args:
        model: SentenceTransformer model
        text: Input text to process
        overlap_ratio: How much to overlap the windows (e.g., 0.25 for 25% overlap)
    
    Returns:
        List of embeddings for each window
    """
    tokenizer = model.tokenizer
    tokens = tokenizer.encode(text, add_special_tokens=False)
    context_size = model.max_seq_length
    effective_window = context_size - tokenizer.num_special_tokens_to_add()
    overlap = int(context_size * overlap_ratio)
    step = effective_window - overlap
    
    chunks = []
    for start in range(0, len(tokens), step):
        end = start + effective_window
        chunk_tokens = tokens[start:end]
        
        # Convert back to text (properly handles BPE/subword tokens)
        chunk_text = tokenizer.decode(chunk_tokens, clean_up_tokenization_spaces=True)
        chunks.append(chunk_text)
    
    return model.encode(chunks)


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


def print_article_details(article):
    """
    Print the details of an article.
    
    Args:
        article (Article): The article object to print.
    """
    if article:
        print(f"Source: {article.source}")
        print(f"Article ID: {article.article_id}")
        print(f"Title: {article.article_title}")
        print(f"Body: {article.article_body}")
        print(f"Part: {article.part}")
        print(f"Title (Group): {article.title}")
        print(f"Chapter: {article.chapter}")
        print(f"Section: {article.section}")
        print("-" * 40)
    else:
        print("Article not found.")


def main():
    model = SentenceTransformer('BlackKakapo/stsb-xlm-r-multilingual-ro')

    print("Fetching all articles...")
    all_articles = get_all_articles()
    for article in all_articles:
        embeddings = get_embeddings(model, article.article_body)
        print(embeddings.shape)


if __name__ == '__main__':
    main()
