from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    # Increase default to cover long focus sessions; can still be overridden via .env
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
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

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
