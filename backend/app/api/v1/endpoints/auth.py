from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Annotated
from app.db.models.user import User
from app.core.responses import success_response, error_response
from app.schemas.auth import EmailLoginForm, EmailRegisterForm
from app.domain.services.auth_service import register_user, authenticate_user, oauth_login
from app.core.dependencies import get_password_hasher, get_token_service, get_google_provider, get_user_repository, get_log_publisher
from app.core.interfaces import PasswordHasher, TokenService, OAuthProvider, UserRepository, LogPublisher
from app.core.security import get_current_user
from app.domain.exceptions.auth_exceptions import InvalidCredentialsError, EmailAlreadyRegisteredError

router = APIRouter()



@router.post("/register")
async def register(
    form_data: Annotated[EmailRegisterForm, Depends(EmailRegisterForm.as_form)],
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    log_publisher: LogPublisher = Depends(get_log_publisher),
    request: Request = None
):
    client_ip = request.client.host if request and request.client else "unknown"

    try:
        await register_user(
            form_data=form_data,
            user_repo=user_repo,
            hasher=hasher,
            client_ip=client_ip,
            log_publisher=log_publisher
        )
        return success_response("User registered successfully")

    except EmailAlreadyRegisteredError as e:
        return error_response(str(e), status_code=409)




@router.post("/login")
async def login(
    form_data: Annotated[EmailLoginForm, Depends(EmailLoginForm.as_form)],
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service),
    log_publisher: LogPublisher = Depends(get_log_publisher),
    request: Request = None
):
    client_ip = request.client.host if request and request.client else "unknown"
    try:
        token_data = await authenticate_user(
            form_data=form_data,
            user_repo=user_repo,
            hasher=hasher,
            token_service=token_service,
            client_ip=client_ip,
            log_publisher=log_publisher
        )
        
        return success_response("Authenticated successfully", data=token_data)

    except InvalidCredentialsError as e:
        return error_response(str(e), status_code=401)
    
    

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