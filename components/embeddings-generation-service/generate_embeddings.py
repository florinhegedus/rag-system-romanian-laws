from common.postgres_db import Session, Article
from sentence_transformers import SentenceTransformer


def get_embeddings(model, text):
    """
    Generate embeddings for a list of sentences using the SentenceTransformer model.
    
    Args:
        sentences (list): A list of sentences to generate embeddings for.
    
    Returns:
        list: A list of embeddings corresponding to the input sentences.
    """
    tokenizer = model.tokenizer
    sentences = text.split('.')

    chunks = [[]]
    chunk_length = 0
    for i, sentence in enumerate(sentences):
        tokens = tokenizer(sentence, padding='longest', return_tensors="pt")
        num_tokens = len(tokens['input_ids'][0]) - 2 # Subtracting 2 for [CLS] and [SEP] tokens
        print(f"Sentence - number of tokens: {num_tokens}")
        if num_tokens > model.max_seq_length:
            print(f"Number of tokens ({num_tokens}) exceeds the maximum sequence length ({model.max_seq_length}).")
            words = sentence.split(' ')
            # TODO: append to curr_chunk and remaining to next chunks
            raise ValueError(f"Sentence exceeds max length: {sentence}")
        elif chunk_length + num_tokens + 2 < model.max_seq_length:
            chunks[-1].append(sentence)
            chunk_length += num_tokens
        else:
            chunks.append([sentence])
            chunk_length = num_tokens

    chunks = ['.'.join(chunk) for chunk in chunks]
    print(f"Number of chunks: {len(chunks)}")

    tokens = tokenizer(chunks, padding='longest', return_tensors="pt")
    tokens.to(model.device)
    embeddings = model(tokens)
    return embeddings


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
    # Example usage of sentence transformer
    model = SentenceTransformer('BlackKakapo/stsb-xlm-r-multilingual-ro')
    text = "This is an example sentence. This is another example sentence."
    embeddings = get_embeddings(model, text)
    print(embeddings['input_ids'][0].shape)

    print("Fetching all articles...")
    all_articles = get_all_articles()
    for article in all_articles:
        embeddings = get_embeddings(model, article.article_body)
        print(embeddings['input_ids'][0].shape)

    # Get tokenizer

    # Count tokens per article

    # curr_chunk article

    # Generate embeddings


if __name__ == '__main__':
    main()
