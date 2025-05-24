from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.auth import UserAuthForm, OAuth2EmailRequestForm
from app.services.user_service import register_user, authenticate_user
from app.services.google_auth_service import google_authenticate
from app.core.dependencies import get_password_hasher, get_token_service
from app.core.interfaces import PasswordHasher, TokenService
from app.core.security import get_current_user

router = APIRouter()


@router.post("/register")
async def register(
    form_data: Annotated[UserAuthForm, Depends(UserAuthForm.as_form)],
    db: AsyncSession = Depends(get_db),
    hasher: PasswordHasher = Depends(get_password_hasher),
):
    return await register_user(form_data, db, hasher)


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2EmailRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
    hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service),
):
    return await authenticate_user(form_data, db, hasher, token_service)


@router.post("/google_auth")
async def auth_google(
    payload: dict,
    db: AsyncSession = Depends(get_db),
    token_service: TokenService = Depends(get_token_service),
):
    return await google_authenticate(payload, db, token_service)


@router.get("/me")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    return {"message": f"Hello, {current_user.email}"}