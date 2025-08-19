# app/api/endpoints/sentiment.py

from fastapi import APIRouter, Depends
from sqlmodel import Session, SQLModel

from app.api import deps
from app.models.sentiment import SearchTerm
from app.models.user import User # <-- 1. IMPORTE O MODELO User
from app.worker.celery_worker import run_sentiment_analysis

class SearchTermCreate(SQLModel):
    term: str

router = APIRouter()

@router.post("/", response_model=SearchTerm)
def start_sentiment_analysis(
    term_in: SearchTermCreate,
    db: Session = Depends(deps.get_db),
    # 2. ADICIONE A DEPENDÊNCIA DO USUÁRIO ATUAL
    current_user: User = Depends(deps.get_current_user) 
):
    """
    Inicia uma nova análise de sentimento para um termo de busca.
    Requer autenticação.
    """
    db_search_term = SearchTerm(term=term_in.term)
    # 3. USE O ID DO USUÁRIO LOGADO, NÃO UM VALOR FIXO
    db_search_term.user_id = current_user.id

    db.add(db_search_term)
    db.commit()
    db.refresh(db_search_term)

    run_sentiment_analysis.delay(db_search_term.id)
    
    return db_search_term