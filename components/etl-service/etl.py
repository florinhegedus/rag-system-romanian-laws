from bs4 import BeautifulSoup
from common import MinIOClient, LegalDocEnum
from common.postgres_db import Session, Article


def save_legal_doc_to_postgres(document_name, minio_client, bucket_name):
    """
    Fetches the legal document from MinIO, parses it, and saves the articles to PostgreSQL.

    :param document_name: Name of the document (e.g., "CODUL_PENAL").
    :param minio_client: An instance of the MinIOClient class.
    :param bucket_name: Name of the MinIO bucket where the document is stored.
    """
    # Fetch the HTML content from MinIO
    object_name = f"{document_name}.html"
    content = minio_client.get_object(bucket_name, object_name)

    if not content:
        print(f"Failed to retrieve {object_name} from MinIO.")
        return

    # Parse the HTML content
    soup = BeautifulSoup(content, 'lxml')

    # Extract all S_ART tags
    articles = soup.find_all('span', attrs={'class': 'S_ART'})

    # Iterate over each article and get ('Part', 'Title', 'Chapter', 'Section')
    look_for = ['S_PRT_TTL', 'S_PRT_DEN', 'S_TTL_TTL', 'S_TTL_DEN', 'S_CAP_TTL', 'S_CAP_DEN', 'S_SEC_TTL', 'S_SEC_DEN']
    session = Session()
    try:
        for article in articles:
            source = document_name
            article_id = article.attrs['id']
            article_title = article.contents[1].text
            article_body = article.contents[3].text
            part = None
            title = None
            chapter = None
            section = None

            # Traverse parents to find chapter and section
            for parent in article.parents:
                # Check parent and siblings of the parent
                for sibling in parent.self_and_previous_siblings:
                    if sibling.name == 'span' and 'class' in sibling.attrs and sibling.attrs['class'][0] in look_for:
                        if 'S_PRT_TTL' in sibling.attrs['class']:
                            part = sibling.text.strip()
                        if 'S_TTL_TTL' in sibling.attrs['class']:
                            title = sibling.text.strip()
                        if 'S_CAP_TTL' in sibling.attrs['class']:
                            chapter = sibling.text.strip()
                        elif 'S_SEC_TTL' in sibling.attrs['class']:
                            section = sibling.text.strip()
                    if part and title and chapter and section:
                        break

            # Check if the article already exists for the given source
            existing_article = session.query(Article).filter_by(source=source, article_id=article_id).first()

            if existing_article:
                print(f"Article with ID {article_id} from source {source} already exists. Updating the article...")
                # Update the existing article
                existing_article.article_title = article_title
                existing_article.article_body = article_body
                existing_article.part = part
                existing_article.title = title
                existing_article.chapter = chapter
                existing_article.section = section
            else:
                # Create a new Article object
                new_article = Article(
                    source=source,
                    article_id=article_id,
                    article_title=article_title,
                    article_body=article_body,
                    part=part,
                    title=title,
                    chapter=chapter,
                    section=section
                )
                # Add the new article to the session
                session.add(new_article)

        # Commit the session to save the articles to the database
        session.commit()
        print(f"{document_name} - Scraping and saving to database terminated successfully.")
    finally:
        session.close()


def main():
    # Initialize MinIO client
    minio_client = MinIOClient()
    bucket_name = "legal-docs-minio-bucket"

    # Process each legal document
    for doc in LegalDocEnum:
        save_legal_doc_to_postgres(doc.name, minio_client, bucket_name)


if __name__ == '__main__':
    main()
