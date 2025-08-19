# app/core/security.py

from datetime import datetime, timedelta
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Contexto para hashing de senhas. bcrypt é o padrão recomendado.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto simples corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(password)

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    """Cria um token de acesso JWT com tempo de expiração."""
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> str | None:
    """Decodifica um token JWT e retorna o 'subject' (e-mail do usuário)."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None