from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.hash_data import BcryptHasher, JWTTokenService
from app.db.session import get_db
from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.interfaces.oauth_account_repository import OAuthAccountRepository
from app.domain.interfaces.oauth_provider import OAuthProvider
from app.domain.interfaces.password_hasher import PasswordHasher
from app.domain.interfaces.sprint_repository import ISprintRepository
from app.domain.interfaces.token_service import TokenService
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.messaging.rabbitmq.rabbitmq_publisher import (
    RabbitMQLogPublisher,
)
from app.infrastructure.oauth_providers.google_provider import GoogleOAuthProvider
from app.infrastructure.repositories.sqla_sprint_saver import (
    SQLAlchemySprintSaverRepository,
)
from app.infrastructure.repositories.sqlalchemy_user_provider import (
    SQLAlchemyOAuthAccountRepository,
    SQLAlchemyUserRepository,
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


def get_sprint_repository(
    session: AsyncSession = Depends(get_db),
) -> ISprintRepository:
    return SQLAlchemySprintSaverRepository(session)
