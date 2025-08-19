import os
import praw
from celery import Celery
from dotenv import load_dotenv
from sqlmodel import Session, select
from app.core.database import engine
from app.models.sentiment import SearchTerm, Post
from app.core.config import settings
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery(__name__, broker=redis_url, backend=redis_url)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)

@celery.task
def run_sentiment_analysis(search_term_id: int):
    """
    Busca posts no Reddit usando PRAW, analisa o sentimento e salva no banco.
    """
    with Session(engine) as session:
        search_term = session.get(SearchTerm, search_term_id)
        if not search_term:
            return f"Termo de busca com ID {search_term_id} não encontrado."

        # 1. Conecta-se à API do Reddit
        reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT,
        )

        # 2. Busca os 15 posts mais relevantes no subreddit 'all'
        subreddit = reddit.subreddit("all")
        submissions = subreddit.search(search_term.term, limit=15)

        analyzer = SentimentIntensityAnalyzer()
        posts_processed = 0

        # 3. Itera sobre os posts encontrados
        for submission in submissions:
            # Verifica se já salvamos este post para evitar duplicatas
            statement = select(Post).where(Post.post_id == submission.id)
            if session.exec(statement).first():
                continue

            text_to_analyze = f"{submission.title}. {submission.selftext}"
            scores = analyzer.polarity_scores(text_to_analyze)
            
            label = "neutro"
            if scores['compound'] >= 0.05:
                label = "positivo"
            elif scores['compound'] <= -0.05:
                label = "negativo"

            # 4. Cria o objeto Post com dados reais
            new_post = Post(
                text=text_to_analyze[:1000], # Limita o texto para caber no DB
                sentiment_score=scores['compound'],
                sentiment_label=label,
                post_id=submission.id,
                source="reddit",
                url=f"https://reddit.com{submission.permalink}",
                search_term_id=search_term.id
            )
            session.add(new_post)
            posts_processed += 1
        
        session.commit()
        return f"Análise para '{search_term.term}' concluída. {posts_processed} novos posts do Reddit foram processados."