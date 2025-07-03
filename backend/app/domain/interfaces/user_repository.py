from typing import Protocol

from app.domain.entities.user import User


class UserRepository(Protocol):
    async def get_user_by_email(self, email: str) -> User | None: ...
    async def create_user(
        self, email: str, hashed_password: str, auth_provider: str
    ) -> User: ...
