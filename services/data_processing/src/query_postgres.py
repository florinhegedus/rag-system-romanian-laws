from core.postgres_db import Session, Article


def get_article_by_id(source, article_id):
    """
    Retrieve an article by its source and article_id.
    
    Args:
        source (str): The source of the article.
        article_id (str): The article_id to search for.
    
    Returns:
        Article: The article object if found, otherwise None.
    """
    session = Session()
    try:
        return session.query(Article).filter_by(source=source, article_id=article_id).first()
    finally:
        session.close()


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
        print(f"Link: {article.link}")
        print("-" * 40)
    else:
        print("Article not found.")


def main():
    # Example usage of the utility functions
    print("Fetching all articles...")
    all_articles = get_all_articles()
    for article in all_articles:
        print_article_details(article)

    print("\nFetching articles from a specific source...")
    specific_source = "CODUL_FISCAL"  # Replace with the source you want to filter by
    articles_from_source = get_all_articles(source=specific_source)
    for article in articles_from_source:
        print_article_details(article)

    print("\nFetching a specific article by source and ID...")
    specific_source = "CODUL_PENAL"  # Replace with the source you want to search for
    specific_article_id = "id_artA155"  # Replace with the article_id you want to search for
    article = get_article_by_id(source=specific_source, article_id=specific_article_id)
    print_article_details(article)

if __name__ == '__main__':
    main()
