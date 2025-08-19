from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

class SearchTermBase(SQLModel):
    term: str = Field(index=True)

class SearchTerm(SearchTermBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="search_terms")
    posts: List["Post"] = Relationship(back_populates="search_term")

class PostBase(SQLModel):
    text: str
    sentiment_score: float = 0.0
    sentiment_label: str = "neutro"

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: str = Field(unique=True, index=True)
    source: str
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    search_term_id: int = Field(foreign_key="searchterm.id")
    search_term: Optional["SearchTerm"] = Relationship(back_populates="posts")

class PostRead(PostBase):
    id: int
    post_id: str
    source: str
    url: str
    created_at: datetime

class SearchTermRead(SearchTermBase):
    id: int
    created_at: datetime

class SearchTermReadWithPosts(SearchTermRead):
    posts: list[PostRead] = []