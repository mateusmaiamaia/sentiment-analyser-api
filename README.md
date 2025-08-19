# 🚀 Plataforma de Análise de Sentimento

## Descrição do Projeto

Este é o backend de uma plataforma de análise de sentimento para mídias sociais. O projeto utiliza **FastAPI** para construir uma API de alta performance que coleta e processa dados do **Reddit**, analisa o sentimento (positivo, negativo ou neutro) e armazena os resultados.

A arquitetura do projeto foi pensada para ser escalável e robusta, empregando **Docker** e **Docker Compose** para conteinerização, e **Celery** com **Redis** para o processamento assíncrono de tarefas pesadas.

---

## 🛠️ Tecnologias Utilizadas

* **Backend**: Python, FastAPI
* **Banco de Dados**: PostgreSQL
* **Conteinerização**: Docker, Docker Compose
* **Processamento Assíncrono**: Celery, Redis
* **Análise de Sentimento**: `vaderSentiment`
* **Coleta de Dados**: `PRAW` (API do Reddit)

---

## ✅ Checklist de Atividades

Esta lista detalha o progresso do projeto e as próximas etapas.

#### **1. Estrutura e Autenticação (100% Concluído)**
* [x] Estrutura inicial de pastas.
* [x] Configuração de variáveis de ambiente.
* [x] Modelos de dados para usuários com **SQLModel**.
* [x] Autenticação de usuário com hashing de senhas.
* [x] Geração e validação de tokens **JWT**.
* [x] Rotas de cadastro e login.

#### **2. Funcionalidades Principais (Em Andamento)**
* [ ] Modelos de dados para as análises (`Analysis`, `SentimentResult`, `Post`).
* [ ] Lógica de coleta de dados do Reddit.
* [ ] Lógica de análise de sentimento com `vaderSentiment`.
* [ ] Rotas da API para iniciar a análise e consultar os resultados.
* [ ] Proteção de rotas com autenticação JWT.

#### **3. Conteinerização e Workers (Pendente)**
* [ ] Configuração do **Redis** e **Celery**.
* [ ] Criação do `Dockerfile` para a aplicação.
* [ ] Criação do `docker-compose.yml` para orquestrar todos os serviços.

---

## ⚙️ Como Rodar o Projeto

*Instruções serão adicionadas aqui após a conclusão da etapa de conteinerização.*

---
