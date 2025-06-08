from datetime import timedelta
from typing import Protocol

from app.core.logging.events import LogEvent
from app.domain.entities.user import User
from app.domain.value_objects.user import UserPasswordHash


class PasswordHasher(Protocol):
    def hash(self, password: str) -> UserPasswordHash: ...
    def verify(
        self, plain_password: str, hashed_password: UserPasswordHash
    ) -> bool: ...


class TokenService(Protocol):
    def create_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str: ...
    def verify_token(self, token: str) -> dict | None: ...


class UserRepository(Protocol):
    async def get_user_by_email(self, email: str) -> User | None: ...
    async def create_user(
        self, email: str, hashed_password: str, auth_provider: str
    ) -> User: ...


class OAuthAccountRepository(Protocol):
    async def get_user_by_oauth(
        self, provider: str, provider_id: str
    ) -> User | None: ...

    async def create_oauth_user(self, email: str, auth_provider: str) -> User: ...

    async def create_oauth_account(
        self, provider: str, provider_id: str, user: User
    ) -> User: ...


class OAuthProvider(Protocol):
    name: str

    async def exchange_code_for_token(self, code: str) -> dict: ...
    async def get_user_info(self, access_token: str) -> dict: ...


class LogPublisher(Protocol):
    async def publish(self, event: LogEvent) -> None: ...
