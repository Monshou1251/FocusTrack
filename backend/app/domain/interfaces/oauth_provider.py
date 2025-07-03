from typing import Protocol


class OAuthProvider(Protocol):
    name: str

    async def exchange_code_for_token(self, code: str) -> dict: ...
    async def get_user_info(self, access_token: str) -> dict: ...
