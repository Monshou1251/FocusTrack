from app.db.session import get_db
from app.core.config import settings


import httpx

CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
GOOGLE_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI

async def exchange_code_for_token(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    print("Sending to Google:", data)

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        print("Response text:", response.text)
        response.raise_for_status()
        return response.json()
