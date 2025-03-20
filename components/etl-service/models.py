from sqlalchemy import create_engine, Column, String, Text, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL (replace with your actual database credentials)
DATABASE_URL = "postgresql+psycopg2://yourusername:yourpassword@postgres:5432/yourdatabase"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured Session class
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define the Article class
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False)
    article_id = Column(String, nullable=False)
    article_title = Column(String, nullable=False)
    article_body = Column(Text, nullable=False)
    part = Column(String)
    title = Column(String)
    chapter = Column(String)
    section = Column(String)

    __table_args__ = (UniqueConstraint('source', 'article_id', name='_source_article_id_uc'),)

# Create all tables in the database (if they don't already exist)
Base.metadata.create_all(engine)
