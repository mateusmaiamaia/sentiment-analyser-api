# app/api/deps.py

from app.core.database import get_session

# Esta é a dependência que suas rotas irão importar e usar
get_db = get_session