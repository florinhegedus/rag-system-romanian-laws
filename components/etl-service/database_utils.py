from models import Article, Session


def get_article_by_id(article_id):
    """
    Retrieve an article by its article_id.
    
    Args:
        article_id (str): The article_id to search for.
    
    Returns:
        Article: The article object if found, otherwise None.
    """
    session = Session()
    try:
        return session.query(Article).filter_by(article_id=article_id).first()
    finally:
        session.close()


def get_all_articles():
    """
    Retrieve all articles from the database.
    
    Returns:
        List[Article]: A list of all Article objects in the database.
    """
    session = Session()
    try:
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
    # Example usage of the utility functions
    print("Fetching all articles...")
    all_articles = get_all_articles()
    for article in all_articles:
        print_article_details(article)

    print("\nFetching a specific article by ID...")
    specific_article_id = 'id_artA155'  # Replace with the article_id you want to search for
    article = get_article_by_id(specific_article_id)
    print_article_details(article)


if __name__ == '__main__':
    main()
