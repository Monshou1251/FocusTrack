from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse

from app.core.dependencies import (
    get_google_provider,
    get_log_publisher,
    get_oauth_account_repository,
    get_password_hasher,
    get_token_service,
    get_user_repository,
)
from app.core.interfaces import (
    LogPublisher,
    OAuthAccountRepository,
    OAuthProvider,
    PasswordHasher,
    TokenService,
    UserRepository,
)
from app.core.responses import error_response, success_response

# from app.core.security import get_current_user
# from app.db.models.user import User
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.domain.services.auth_service import (
    authenticate_oauth_user,
    authenticate_user,
    register_user,
)
from app.schemas.auth import EmailLoginForm, EmailRegisterForm

router = APIRouter()


@router.post("/register")
async def register(
    request: Request,
    form_data: Annotated[EmailRegisterForm, Form()],
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    log_publisher: LogPublisher = Depends(get_log_publisher),
) -> JSONResponse:
    client_ip = request.client.host if request and request.client else "unknown"

    try:
        await register_user(
            form_data=form_data,
            user_repo=user_repo,
            hasher=hasher,
            client_ip=client_ip,
            log_publisher=log_publisher,
        )
        return success_response("User registered successfully")

    except EmailAlreadyRegisteredError as e:
        return error_response(str(e), status_code=409)


@router.post("/login")
async def login(
    request: Request,
    form_data: Annotated[EmailLoginForm, Form()],
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service),
    log_publisher: LogPublisher = Depends(get_log_publisher),
) -> JSONResponse:
    client_ip = request.client.host if request and request.client else "unknown"
    try:
        token_data = await authenticate_user(
            form_data=form_data,
            user_repo=user_repo,
            hasher=hasher,
            token_service=token_service,
            client_ip=client_ip,
            log_publisher=log_publisher,
        )

        return success_response("Authenticated successfully", data=token_data)

    except InvalidCredentialsError as e:
        return error_response(str(e), status_code=401)


@router.post("/google_auth")
async def auth_google(
    request: Request,
    payload: dict,
    token_service: TokenService = Depends(get_token_service),
    provider: OAuthProvider = Depends(get_google_provider),
    user_repo: UserRepository = Depends(get_user_repository),
    oauth_repo: OAuthAccountRepository = Depends(get_oauth_account_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
) -> JSONResponse:
    client_ip = request.client.host if request and request.client else "unknown"
    try:
        token_data = await authenticate_oauth_user(
            payload["code"],
            provider,
            token_service,
            user_repo,
            oauth_repo,
            client_ip,
            log_publisher,
        )
        return success_response("Authenticated via OAuth", data=token_data)
    except InvalidCredentialsError:
        return error_response("OAuth authentication failed", status_code=400)


# @router.get("/me")
# async def protected_route(current_user: User = Depends(get_current_user)):
#     return {"message": f"Hello, {current_user.email}"}
