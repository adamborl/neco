import os

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///articles.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Article(Base):
    """Database model for stored articles."""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    published_at = Column(DateTime)
    source_url = Column(String, unique=True, nullable=False)


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(engine)
