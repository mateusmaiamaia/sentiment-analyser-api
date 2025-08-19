# app/models/user.py

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

# from app.models.sentiment import SearchTerm  <-- REMOVA ESTA LINHA

class UserBase(SQLModel):
    """Esquema base para o usuário."""
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

class User(UserBase, table=True):
    """Modelo de tabela para o usuário."""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    # Coloque "SearchTerm" entre aspas
    search_terms: List["SearchTerm"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    """Esquema de criação de usuário (inclui a senha)."""
    password: str

class UserRead(UserBase):
    """Esquema de leitura de usuário."""
    id: int