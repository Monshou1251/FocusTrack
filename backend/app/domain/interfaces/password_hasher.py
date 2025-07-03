from typing import Protocol

from app.domain.value_objects.user import UserPasswordHash


class PasswordHasher(Protocol):
    def hash(self, password: str) -> UserPasswordHash: ...
    def verify(
        self, plain_password: str, hashed_password: UserPasswordHash
    ) -> bool: ...
