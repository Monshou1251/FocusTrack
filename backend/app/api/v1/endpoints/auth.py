from fastapi import APIRouter, Depends
from typing import Annotated
from app.db.models.user import User
from app.schemas.auth import OAuth2EmailRequestForm
from app.services.auth_service import register_user, authenticate_user, oauth_login
from app.core.dependencies import get_password_hasher, get_token_service, get_google_provider, get_user_repository
from app.core.interfaces import PasswordHasher, TokenService, OAuthProvider, UserRepository
from app.core.security import get_current_user

router = APIRouter()


@router.post("/register")
async def register(
    form_data: Annotated[OAuth2EmailRequestForm, Depends()],
    hasher: PasswordHasher = Depends(get_password_hasher),
    user_repo: UserRepository = Depends(get_user_repository)
):
    return await register_user(form_data, user_repo, hasher)


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2EmailRequestForm, Depends()],
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service),
):
    return await authenticate_user(form_data, user_repo, hasher, token_service)


@router.post("/google_auth")
async def auth_google(
    payload: dict,
    token_service = Depends(get_token_service),
    provider: OAuthProvider = Depends(get_google_provider),
    user_repo: UserRepository = Depends(get_user_repository),
):
    return await oauth_login(payload["code"], provider, token_service, user_repo)


@router.get("/me")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    return {"message": f"Hello, {current_user.email}"}