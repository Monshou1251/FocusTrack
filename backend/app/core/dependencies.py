from app.core.interfaces import PasswordHasher, TokenService, OAuthProvider, UserRepository, LogPublisher
from app.core.security import BcryptHasher, JWTTokenService
from app.infrastructure.auth_providers.google_provider import GoogleOAuthProvider
from app.infrastructure.auth_providers.sqlalchemy_user_provider import SQLAlchemyUserRepository
from app.db.session import get_db
from app.infrastructure.messaging.rabbitmq.rabbitmq_publisher import RabbitMQLogPublisher
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends



def get_password_hasher() -> PasswordHasher:
    return BcryptHasher()

def get_token_service() -> TokenService:
    return JWTTokenService()

def get_google_provider() -> OAuthProvider:
    return GoogleOAuthProvider()

def get_user_repository(
    db: AsyncSession = Depends(get_db)    
) -> UserRepository:
    return SQLAlchemyUserRepository(db)

def get_log_publisher() -> LogPublisher:
    return RabbitMQLogPublisher()
