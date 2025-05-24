from sqlalchemy.ext.asyncio import AsyncSession
from app.core.interfaces import TokenService
# from app.core.security import decode_google_id_token
from app.core.config import settings
from app.core.google_auth_security import exchange_code_for_token



async def google_authenticate(payload: dict, db: AsyncSession, token_service: TokenService):
    code = payload["code"]

    token_data = await exchange_code_for_token(code)
    print("token_data")
    print(token_data)
    # id_token = token_data["id_token"]
    # claims = decode_google_id_token(id_token)
    
    # email = claims["email"]
    # name = claims.get("name")

    # user = await get_user_by_email(db, email)
    # if not user:
    #     user = await create_user_from_google(db, email=email, name=name)

    # return await token_service.create_tokens_for_user(user)
