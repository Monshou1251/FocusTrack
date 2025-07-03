# app\infrastructure\repositories\google_provider.py

import httpx

from app.core.config import settings
from app.domain.interfaces.oauth_provider import OAuthProvider


class GoogleOAuthProvider(OAuthProvider):
    name = "google"

    async def exchange_code_for_token(self, code: str) -> dict:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            return response.json()

    async def get_user_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                params={"access_token": access_token},
            )
            response.raise_for_status()
            return response.json()
