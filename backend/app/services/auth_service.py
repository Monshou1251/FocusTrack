from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User, OAuthAccount
from app.schemas.auth import OAuth2EmailRequestForm
from app.core.interfaces import PasswordHasher, TokenService, OAuthProvider, UserRepository
import pprint


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login') 


from fastapi import status

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
            return {
                "success": False,
                "error": "Email already registered through OAuth"
            }
        else:
            return {
                "success": False,
                "error": "Email already registered"
            }

    hashed_password = hasher.hash(password)
    await user_repo.create_user(email, hashed_password, auth_provider="email")

    return {
        "success": True,
        "message": "User created successfully."
    }



async def authenticate_user(
    form_data: OAuth2EmailRequestForm,
    user_repo: UserRepository,
    hasher: PasswordHasher,
    token_service: TokenService
):
    user = await user_repo.get_user_by_email(form_data.email)

    if not user or not hasher.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = token_service.create_token({"sub": user.email})
    
    return {"access_token": token, "token_type": "bearer"}


async def oauth_login(
    code: str,
    oauth_provider: OAuthProvider,
    token_service: TokenService,
    user_repo: UserRepository,
):
    token_data = await oauth_provider.exchange_code_for_token(code)
    access_token = token_data["access_token"]
    user_info = await oauth_provider.get_user_info(access_token)

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
    return {"access_token": token, "token_type": "bearer"}




async def get_current_user(token):
    pass
