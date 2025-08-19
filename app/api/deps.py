# app/api/deps.py

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlmodel import Session

from app.core.database import engine, get_session
from app.core.config import settings
from app.models.user import User

# Este é o esquema de segurança que aparecerá no /docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

class TokenData(BaseModel):
    sub: str | None = None

def get_db() -> Generator[Session, None, None]:
    """Retorna uma sessão de banco de dados."""
    with Session(engine) as session:
        yield session

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Decodifica o token JWT para obter o usuário atual.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(sub=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user