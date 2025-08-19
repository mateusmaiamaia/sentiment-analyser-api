# app/api/endpoints/users.py

from typing import Annotated
from datetime import timedelta  # <-- ADICIONADO: Para definir a expiração do token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.api import deps
from app.models.user import User, UserCreate, UserRead
from app.core.security import get_password_hash, create_access_token, verify_password
from app.core.config import settings # <-- ADICIONADO: Para acessar as configurações

router = APIRouter(prefix="/users", tags=["users"])

# REMOVIDO: Função get_db local, pois agora importamos a dependência de deps.py

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(deps.get_db)): # <-- ALTERADO
    """Cria um novo usuário."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado."
        )

    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(deps.get_db) # <-- ALTERADO
):
    """Autentica o usuário e retorna um token de acesso."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}