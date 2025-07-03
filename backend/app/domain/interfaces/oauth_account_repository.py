from typing import Protocol

from app.domain.entities.user import User


class OAuthAccountRepository(Protocol):
    async def get_user_by_oauth(
        self, provider: str, provider_id: str
    ) -> User | None: ...

    async def create_oauth_user(
        self, email: str, auth_provider: str, avatar_url: str | None
    ) -> User: ...

    async def create_oauth_account(
        self, provider: str, provider_id: str, user: User
    ) -> User: ...
