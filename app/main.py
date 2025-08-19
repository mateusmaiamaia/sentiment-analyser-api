# app/main.py

from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.api.api_router import router as api_router

def create_app():
    app = FastAPI(title="Plataforma de Análise de Sentimento")

    # Garante que as tabelas do banco de dados sejam criadas
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    @app.get("/")
    def read_root():
        return {"message": "Bem-vindo à API de Análise de Sentimento!"}
        
    app.include_router(api_router)
    
    return app

app = create_app()