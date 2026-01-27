from typing import Protocol, Optional


class OAuthProvider(Protocol):
    name: str

    async def exchange_code_for_token(self, code: str, redirect_uri: Optional[str] = None) -> dict: ...
    async def get_user_info(self, access_token: str) -> dict: ...
