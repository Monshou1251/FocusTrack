from pathlib import Path

from dotenv import load_dotenv

# Вычисляем абсолютный путь до backend/.env
env_path = Path(__file__).resolve().parents[2] / ".env"

# Загружаем .env
load_dotenv(dotenv_path=env_path)
