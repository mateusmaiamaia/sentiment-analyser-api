# app/api/api_router.py

from fastapi import APIRouter
from app.api.endpoints import users, sentiment # <-- 1. IMPORTE AQUI

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"]) # <-- 2. INCLUA AQUI