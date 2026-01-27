from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # Environment
    ENVIRONMENT: str = "development"

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"

    # Email
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str

    # OAuth
    CLIENT_ID: str
    CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    RABBITMQ_LOG_QUEUE: str = "log_queue"

    # JWT Settings
    JWT_EXPIRATION_DAYS: int = 7

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"

    @property
    def jwt_max_age_seconds(self) -> int:
        """Get JWT expiration in seconds"""
        return self.JWT_EXPIRATION_DAYS * 24 * 60 * 60

    @property
    def secure_cookies(self) -> bool:
        """Enable secure cookies in production"""
        return self.is_production

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
