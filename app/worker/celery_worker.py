# app/worker/celery_worker.py

import os
from celery import Celery
from dotenv import load_dotenv
from sqlmodel import Session, select

# Importe o 'engine' para criar sessões de DB e os modelos
from app.core.database import engine
from app.models.sentiment import SearchTerm, Post

# Importe a biblioteca de análise de sentimento
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Cria a instância do Celery
celery = Celery(__name__, broker=redis_url, backend=redis_url)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)

# --- NOVA TAREFA DE ANÁLISE DE SENTIMENTO ---
@celery.task
def run_sentiment_analysis(search_term_id: int):
    """
    Tarefa Celery para executar a análise de sentimento em um termo de busca.
    """
    # Criamos uma sessão de banco de dados exclusiva para esta tarefa
    with Session(engine) as session:
        # 1. Busca o termo de busca no banco de dados
        search_term = session.get(SearchTerm, search_term_id)
        if not search_term:
            return f"SearchTerm com id {search_term_id} não encontrado."

        # 2. Simula a coleta de dados (no futuro, usaremos o Reddit aqui)
        # Por enquanto, vamos analisar o próprio termo como exemplo
        posts_data = [
            {"text": f"Eu amo o termo {search_term.term}, é incrível!", "post_id": "sim_1", "source": "simulation", "url": "#"},
            {"text": f"Eu odeio {search_term.term}, é terrível.", "post_id": "sim_2", "source": "simulation", "url": "#"},
            {"text": f"Não sei o que pensar sobre {search_term.term}.", "post_id": "sim_3", "source": "simulation", "url": "#"}
        ]

        # 3. Analisa o sentimento de cada "post"
        analyzer = SentimentIntensityAnalyzer()
        for post_data in posts_data:
            text_to_analyze = post_data["text"]
            sentiment_scores = analyzer.polarity_scores(text_to_analyze)
            
            # 4. Define o sentimento com base na pontuação composta
            sentiment_label = "neutro"
            if sentiment_scores['compound'] >= 0.05:
                sentiment_label = "positivo"
            elif sentiment_scores['compound'] <= -0.05:
                sentiment_label = "negativo"

            # 5. Cria o objeto Post e salva no banco de dados
            new_post = Post(
                text=text_to_analyze,
                sentiment_score=sentiment_scores['compound'],
                sentiment_label=sentiment_label,
                post_id=post_data["post_id"],
                source=post_data["source"],
                url=post_data["url"],
                search_term_id=search_term.id
            )
            session.add(new_post)
        
        session.commit()
        return f"Análise para '{search_term.term}' concluída. {len(posts_data)} posts processados."