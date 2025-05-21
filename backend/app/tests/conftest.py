import os
from dotenv import load_dotenv
from pathlib import Path

# Вычисляем абсолютный путь до backend/.env
env_path = Path(__file__).resolve().parents[2] / ".env"

# Загружаем .env
load_dotenv(dotenv_path=env_path)
