
from typing import Generator

from sqlmodel import create_engine, Session

from app.core.config import settings

from app.models.user import User  
from app.models.sentiment import SearchTerm, Post  

engine = create_engine(str(settings.DATABASE_URL), echo=True)

def create_db_and_tables():
    """Cria o banco de dados e as tabelas definidas nos modelos."""
    SQLModel.metadata.create_all(engine)
    pass

def get_session() -> Generator[Session, None, None]:
    """Cria uma sessão de banco de dados para ser usada como dependência no FastAPI."""
    with Session(engine) as session:
        yield session