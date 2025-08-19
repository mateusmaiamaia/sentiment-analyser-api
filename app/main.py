# app/main.py

from fastapi import FastAPI
from sqlmodel import SQLModel                 
from app.core.database import engine  
from app.api.api_router import router as api_router

# Importe os modelos para que o SQLModel os reconheça
from app.models.user import User
from app.models.sentiment import SearchTerm, Post

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_app():
    app = FastAPI(title="Plataforma de Análise de Sentimento")

    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    @app.get("/")
    def read_root():
        return {"message": "Bem-vindo à API de Análise de Sentimento!"}
    
    app.include_router(api_router)
    
    return app

app = create_app()