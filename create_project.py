import os

def create_file_with_content(file_path, content=""):
    """Cria um arquivo e escreve o conteúdo nele."""
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Arquivo criado: {file_path}")

def create_directory(dir_path):
    """Cria um diretório se ele não existir."""
    os.makedirs(dir_path, exist_ok=True)
    print(f"Diretório criado: {dir_path}")

def main():
    """Cria a estrutura de pastas e arquivos para o projeto."""
    base_dir = "."
    app_dir = os.path.join(base_dir, "app")
    api_dir = os.path.join(app_dir, "api")
    endpoints_dir = os.path.join(api_dir, "endpoints")
    core_dir = os.path.join(app_dir, "core")
    models_dir = os.path.join(app_dir, "models")
    crud_dir = os.path.join(app_dir, "crud")
    
    # Criar diretórios
    create_directory(endpoints_dir)
    create_directory(core_dir)
    create_directory(models_dir)
    create_directory(crud_dir)

    # Criar arquivos
    create_file_with_content(
        os.path.join(base_dir, "requirements.txt"),
        "fastapi\nuvicorn[standard]\nsqlmodel\npsycopg2-binary\npython-jose[cryptography]\npasslib[bcrypt]\nvaderSentiment\ntweepy"
    )
    create_file_with_content(
        os.path.join(base_dir, ".env"),
        "DATABASE_URL=\nSECRET_KEY=\nTWITTER_BEARER_TOKEN=\nREDIS_URL="
    )
    create_file_with_content(os.path.join(base_dir, "README.md"), "# Plataforma de Análise de Sentimento\n\nEste projeto...")
    
    create_file_with_content(os.path.join(app_dir, "__init__.py"))
    create_file_with_content(os.path.join(api_dir, "__init__.py"))
    create_file_with_content(os.path.join(endpoints_dir, "__init__.py"))
    create_file_with_content(os.path.join(core_dir, "__init__.py"))
    create_file_with_content(os.path.join(models_dir, "__init__.py"))
    create_file_with_content(os.path.join(crud_dir, "__init__.py"))

    create_file_with_content(
        os.path.join(app_dir, "main.py"),
        "from fastapi import FastAPI\nfrom app.core.config import settings\n\napp = FastAPI(title=\"Plataforma de Análise de Sentimento\")\n\n@app.get(\"/\")\ndef read_root():\n    return {\"message\": \"Bem-vindo à API de Análise de Sentimento!\"}\n"
    )

    create_file_with_content(
        os.path.join(core_dir, "config.py"),
        "import os\n\nfrom pydantic_settings import BaseSettings\n\nclass Settings(BaseSettings):\n    DATABASE_URL: str = os.getenv(\"DATABASE_URL\")\n    SECRET_KEY: str = os.getenv(\"SECRET_KEY\")\n    ALGORITHM: str = \"HS256\"\n    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30\n    TWITTER_BEARER_TOKEN: str = os.getenv(\"TWITTER_BEARER_TOKEN\")\n    REDIS_URL: str = os.getenv(\"REDIS_URL\")\n\n    class Config:\n        env_file = \".env\"\n\nsettings = Settings()\n"
    )
    
    # Criar arquivos de endpoints e crud vazios para a estrutura
    create_file_with_content(os.path.join(endpoints_dir, "users.py"))
    create_file_with_content(os.path.join(endpoints_dir, "sentiment.py"))
    create_file_with_content(os.path.join(models_dir, "base.py"))
    create_file_with_content(os.path.join(crud_dir, "users.py"))

    print("\nEstrutura do projeto criada com sucesso!")

if __name__ == "__main__":
    main()