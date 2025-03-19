import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CODUL_PENAL_LINK = "https://legislatie.just.ro/Public/DetaliiDocument/109855"

# Define the Article class for ORM
Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String, unique=True, nullable=False)
    article_title = Column(String, nullable=False)
    article_body = Column(Text, nullable=False)
    part = Column(String)
    title = Column(String)
    chapter = Column(String)
    section = Column(String)

# Set up the database connection
DATABASE_URL = "postgresql+psycopg2://yourusername:yourpassword@localhost:5432/yourdatabase"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def main():
    page = requests.get(CODUL_PENAL_LINK)

    # Save content to file
    with open('CODUL_PENAL.html', 'wb+') as f:
        f.write(page.content)
    
    with open('CODUL_PENAL.html', 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(content, 'lxml')
    
    # Extract all S_ART tags
    articles = soup.find_all('span', attrs={'class': 'S_ART'})

    # Iterate over each article and get ('Part', 'Title', 'Chapter', 'Section')
    look_for = ['S_PRT_TTL', 'S_PRT_DEN', 'S_TTL_TTL', 'S_TTL_DEN', 'S_CAP_TTL', 'S_CAP_DEN', 'S_SEC_TTL', 'S_SEC_DEN']
    for article in articles:
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

        # Create an Article object and add it to the session
        new_article = Article(
            article_id=article_id,
            article_title=article_title,
            article_body=article_body,
            part=part,
            title=title,
            chapter=chapter,
            section=section
        )
        session.add(new_article)

    # Commit the session to save the articles to the database
    session.commit()
    print("Scraping and saving to database terminated successfully.")

if __name__ == '__main__':
    main()