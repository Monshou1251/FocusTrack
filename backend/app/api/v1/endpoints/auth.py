from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import UserAuthForm
from app.services.user_service import register_user, authenticate_user
from app.core.dependencies import get_password_hasher, get_token_service
from app.core.interfaces import PasswordHasher, TokenService


router = APIRouter()


@router.post("/register")
async def register(
    form_data: Annotated[UserAuthForm, Depends()],
    db: AsyncSession = Depends(get_db),
    hasher: PasswordHasher = Depends(get_password_hasher),
):
    return await register_user(form_data, db, hasher)


@router.post("/login")
async def login(
        form_data: Annotated[UserAuthForm, Depends()],
        db: AsyncSession = Depends(get_db),
        hasher: PasswordHasher = Depends(get_password_hasher),
        token_service: TokenService = Depends(get_token_service),
):
    return await authenticate_user(form_data, db, hasher, token_service)
