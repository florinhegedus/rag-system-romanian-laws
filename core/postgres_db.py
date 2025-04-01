import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Text, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Load environment variables from .env file
load_dotenv()


# Set up the database connection parameters
HOST = 'localhost' if os.getenv("ENVIRONMENT") == "local" else 'postgres'
USERNAME = os.getenv("POSTGRES_USER", "default_username")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "default_password")
DATABASE = os.getenv("POSTGRES_DB", "default_database")
DATABASE_URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:5432/{DATABASE}"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
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
