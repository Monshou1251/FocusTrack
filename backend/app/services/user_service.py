from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User, OAuthAccount
from app.schemas.auth import UserAuthForm, OAuth2EmailRequestForm
from app.core.interfaces import PasswordHasher, TokenService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login') 


async def register_user(
    form_data: UserAuthForm,
    db: AsyncSession,
    hasher: PasswordHasher
):
    email = form_data.email
    password = form_data.password
    result = await db.execute(select(User).filter(User.email == email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hasher.hash(password)
    user = User(email=email, hashed_password=hashed_password)
    
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"msg": "User created successfully."}


async def authenticate_user(
    form_data: OAuth2EmailRequestForm,
    db: AsyncSession,
    hasher: PasswordHasher,
    token_service: TokenService
):
    print(form_data)
    result = await db.execute(select(User).filter(User.email == form_data.email))
    user = result.scalars().first()

    if not user or not hasher.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = token_service.create_token({"sub": user.email})
    
    return {"access_token": token, "token_type": "bearer"}


async def google_authenticate(payload: str, db: AsyncSession, token_service: TokenService):
    print("payload")
    print(payload)


async def get_current_user(token):
    pass
