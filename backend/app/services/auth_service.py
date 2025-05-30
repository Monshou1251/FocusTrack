from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User, OAuthAccount
from app.schemas.auth import OAuth2EmailRequestForm
from app.core.interfaces import PasswordHasher, TokenService, OAuthProvider, UserRepository
from app.core.responses import success_response, error_response
from app.messaging.rabbitmq.publisher import publish_log
from datetime import datetime, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login') 


async def register_user(
    form_data: OAuth2EmailRequestForm,
    user_repo: UserRepository,
    hasher: PasswordHasher
):
    email = form_data.email
    password = form_data.password
    
    existing_user = await user_repo.get_user_by_email(email)
    
    if existing_user:
        if existing_user.auth_provider != 'email':
            return error_response("Email already registered through OAuth", status_code=409)

        else:
            return error_response("Email already registered", status_code=409)


    hashed_password = hasher.hash(password)
    await user_repo.create_user(email, hashed_password, auth_provider="email")

    return success_response("User created successfully.")


async def authenticate_user(
    form_data: OAuth2EmailRequestForm,
    user_repo: UserRepository,
    hasher: PasswordHasher,
    token_service: TokenService,
    client_ip: str
):
    user = await user_repo.get_user_by_email(form_data.email)

    success = False  # по умолчанию неуспешно
    if user and hasher.verify(form_data.password, user.hashed_password):
        success = True
        token = token_service.create_token({"sub": user.email})
        response = success_response("Authenticated successfully", data={"access_token": token, "token_type": "bearer"})
    else:
        response = error_response("Incorrect email or password", status_code=401)

    
    publish_log({
        "event": "user_login_attempt",
        "email": form_data.email,
        "success": success,
        "ip": client_ip,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    return response



async def oauth_login(
    code: str,
    oauth_provider: OAuthProvider,
    token_service: TokenService,
    user_repo: UserRepository,
):
    try:
        token_data = await oauth_provider.exchange_code_for_token(code)
        access_token = token_data["access_token"]
        user_info = await oauth_provider.get_user_info(access_token)
    except Exception:
        return error_response("OAuth authentication failed", status_code=400)

    if "id" not in user_info or "email" not in user_info:
        return error_response("Invalid user info from OAuth provider", status_code=400)

    user = await user_repo.get_user_by_oauth(oauth_provider.name, user_info["id"])
    if not user:
        user = await user_repo.get_user_by_email(user_info["email"])
        if not user:
            user = await user_repo.create_oauth_user(
                user_info["email"],
                auth_provider=oauth_provider.name,
            )
        await user_repo.create_oauth_account(
            provider=oauth_provider.name,
            provider_id=user_info["id"],
            user=user,
        )

    token = token_service.create_token({"sub": user.email})
    return success_response("Authenticated via OAuth", data={"access_token": token, "token_type": "bearer"})





async def get_current_user(token):
    pass
