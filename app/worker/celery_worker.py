import os
import tweepy
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
    Busca tweets usando Tweepy, analisa o sentimento e salva no banco.
    """
    with Session(engine) as session:
        search_term = session.get(SearchTerm, search_term_id)
        if not search_term:
            return f"Termo de busca com ID {search_term_id} não encontrado."

        client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)

        query = f'{search_term.term} -is:retweet lang:en'
        response = client.search_recent_tweets(query=query, max_results=15)
        
        tweets = response.data or []
        analyzer = SentimentIntensityAnalyzer()
        posts_processed = 0

        for tweet in tweets:
            statement = select(Post).where(Post.post_id == str(tweet.id))
            if session.exec(statement).first():
                continue

            scores = analyzer.polarity_scores(tweet.text)
            
            label = "neutro"
            if scores['compound'] >= 0.05:
                label = "positivo"
            elif scores['compound'] <= -0.05:
                label = "negativo"

            new_post = Post(
                text=tweet.text,
                sentiment_score=scores['compound'],
                sentiment_label=label,
                post_id=str(tweet.id),
                source="twitter",
                url=f"https://twitter.com/anyuser/status/{tweet.id}",
                search_term_id=search_term.id
            )
            session.add(new_post)
            posts_processed += 1
        
        session.commit()
        return f"Análise para '{search_term.term}' concluída. {posts_processed} novos tweets foram processados."