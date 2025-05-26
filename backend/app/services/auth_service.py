from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User, OAuthAccount
from app.schemas.auth import OAuth2EmailRequestForm
from app.core.interfaces import PasswordHasher, TokenService, OAuthProvider, UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login') 


async def register_user(
    form_data: OAuth2EmailRequestForm,
    user_repo: UserRepository,
    hasher: PasswordHasher
):
    email = form_data.email
    password = form_data.password
    
    if await user_repo.exists_by_email(email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hasher.hash(password)
    await user_repo.create_user(email, hashed_password)

    return {"msg": "User created successfully."}


async def authenticate_user(
    form_data: OAuth2EmailRequestForm,
    user_repo: UserRepository,
    hasher: PasswordHasher,
    token_service: TokenService
):
    user = await user_repo.get_by_email(form_data.email)

    if not user or not hasher.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = token_service.create_token({"sub": user.email})
    
    return {"access_token": token, "token_type": "bearer"}


async def oauth_login(
    code: str,
    db: AsyncSession,
    oauth_provider: OAuthProvider,
    token_service: TokenService
):
    token_data = await oauth_provider.exchange_code_for_token(code)
    access_token = token_data["access_token"]
    user_info = await oauth_provider.get_user_info(access_token)
    print('#'* 10)
    print("user_info")
    print(user_info)
    print('#'* 10)
    # TODO: логика создания/поиска пользователя по email
    # user = await get_or_create_user(user_info, db)

    # Для примера:
    token = token_service.create_token({"sub": user_info["email"]})
    print("token from services/auth_service")
    print(token)
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token):
    pass
