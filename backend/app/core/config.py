from pydantic_settings import BaseSettings
from pydantic import ConfigDict  

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    RABBITMQ_LOG_QUEUE: str = "log_queue"

    model_config = ConfigDict(env_file=".env")

settings = Settings()
