from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, SQLModel, select

from app.api import deps
from app.models.sentiment import SearchTerm, SearchTermRead, SearchTermReadWithPosts
from app.models.user import User
from app.worker.celery_worker import run_sentiment_analysis

class SearchTermCreate(SQLModel):
    term: str

router = APIRouter()

@router.post("/", response_model=SearchTerm)
def start_sentiment_analysis(
    term_in: SearchTermCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_search_term = SearchTerm(term=term_in.term)
    db_search_term.user_id = current_user.id
    db.add(db_search_term)
    db.commit()
    db.refresh(db_search_term)
    run_sentiment_analysis.delay(db_search_term.id)
    return db_search_term

@router.get("/", response_model=List[SearchTermRead])
def get_user_analyses(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    statement = select(SearchTerm).where(SearchTerm.user_id == current_user.id)
    search_terms = db.exec(statement).all()
    return search_terms

@router.get("/{search_term_id}", response_model=SearchTermReadWithPosts)
def get_analysis_results(
    search_term_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    search_term = db.get(SearchTerm, search_term_id)
    
    if not search_term:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Análise não encontrada.")
    
    if search_term.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a ver esta análise.")
        
    return search_term