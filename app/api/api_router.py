# app/api/api_router.py

from fastapi import APIRouter

from app.api.endpoints import users

router = APIRouter()
router.include_router(users.router)