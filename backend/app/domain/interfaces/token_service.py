from datetime import timedelta
from typing import Protocol


class TokenService(Protocol):
    def create_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str: ...
    def verify_token(self, token: str) -> dict | None: ...
