from fastapi import APIRouter, Depends, Request
from app.core.oauth import oauth
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.auth import UserAuthForm, OAuth2EmailRequestForm
from app.services.user_service import register_user, authenticate_user, register_oauth_user
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


# @router.get("/google/login")
# async def login_via_google(request: Request):
#     redirect_uri = request.url_for("auth_google_callback")
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @router.get("/google/callback")
# async def auth_google_callback(request: Request, db: AsyncSession = Depends(get_db)):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = await oauth.google.parse_id_token(request, token)

#     # Зарегистрировать или получить пользователя
#     user = await register_oauth_user(user_info, db)
    
#     # Сгенерировать JWT
#     access_token = create_access_token({"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    return {"message": f"Hello, {current_user.email}"}