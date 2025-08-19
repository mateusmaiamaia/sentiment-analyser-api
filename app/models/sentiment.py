# app/models/sentiment.py

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.user import User  # Importa o modelo de usuário

class SearchTermBase(SQLModel):
    """Esquema base para o termo de busca."""
    term: str = Field(index=True)

class SearchTerm(SearchTermBase, table=True):
    """Modelo de tabela para o termo de busca."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="search_terms")
    posts: List["Post"] = Relationship(back_populates="search_term")

class PostBase(SQLModel):
    """Esquema base para o post."""
    text: str
    sentiment_score: float = 0.0
    sentiment_label: str = "neutro"

class Post(PostBase, table=True):
    """Modelo de tabela para o post."""
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: str = Field(unique=True, index=True)  # ID do post na plataforma (Reddit, Twitter, etc.)
    source: str  # Ex: "reddit", "twitter"
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    search_term_id: int = Field(foreign_key="searchterm.id")
    
    search_term: Optional[SearchTerm] = Relationship(back_populates="posts")