from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces import (
    LogPublisher,
    OAuthAccountRepository,
    OAuthProvider,
    PasswordHasher,
    TokenService,
    UserRepository,
)
from app.core.security import BcryptHasher, JWTTokenService
from app.db.session import get_db
from app.infrastructure.auth_providers.google_provider import GoogleOAuthProvider
from app.infrastructure.auth_providers.sqlalchemy_user_provider import (
    SQLAlchemyOAuthAccountRepository,
    SQLAlchemyUserRepository,
)
from app.infrastructure.messaging.rabbitmq.rabbitmq_publisher import (
    RabbitMQLogPublisher,
)


def get_password_hasher() -> PasswordHasher:
    return BcryptHasher()


def get_token_service() -> TokenService:
    return JWTTokenService()


def get_google_provider() -> OAuthProvider:
    return GoogleOAuthProvider()


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(session)


def get_oauth_account_repository(
    session: AsyncSession = Depends(get_db),
) -> OAuthAccountRepository:
    return SQLAlchemyOAuthAccountRepository(session)


def get_log_publisher() -> LogPublisher:
    return RabbitMQLogPublisher()
