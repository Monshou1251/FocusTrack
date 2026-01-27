import logging
from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, Query, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse

from app.core.config import settings
from app.core.dependencies import (
    get_category_repository,
    get_google_provider,
    get_log_publisher,
    get_oauth_account_repository,
    get_password_hasher,
    get_token_service,
    get_user_repository,
)
from app.core.rate_limiter import limiter
from app.core.responses import error_response, success_response
from app.core.security.user_security import get_current_user
from app.domain.entities.user import User as UserEntity
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.domain.interfaces.category_repository import ICategoryRepository
from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.interfaces.oauth_account_repository import OAuthAccountRepository
from app.domain.interfaces.oauth_provider import OAuthProvider
from app.domain.interfaces.password_hasher import PasswordHasher
from app.domain.interfaces.token_service import TokenService
from app.domain.interfaces.user_repository import UserRepository
from app.domain.services.auth_service import (
    authenticate_oauth_user,
    authenticate_user,
    register_user,
)
from app.domain.services.category_service import (
    create_category_service,
)
from app.schemas.auth import EmailLoginForm, EmailRegisterForm
from app.schemas.user import UserOut

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register")
@limiter.limit("3/hour")
async def register(
    request: Request,
    form_data: Annotated[EmailRegisterForm, Form()],
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    log_publisher: LogPublisher = Depends(get_log_publisher),
    category_repo: ICategoryRepository = Depends(get_category_repository),
) -> JSONResponse:
    client_ip = request.client.host if request and request.client else "unknown"

    try:
        user = await register_user(
            form_data=form_data,
            user_repo=user_repo,
            hasher=hasher,
            client_ip=client_ip,
            log_publisher=log_publisher,
        )

        default_categories = ["Work", "Personal", "Hobbies"]
        for name in default_categories:
            await create_category_service(
                category_repo=category_repo,
                user_id=user.id.value,
                email=user.email.value,
                client_ip=client_ip,
                log_publisher=log_publisher,
                name=name,
            )
        return success_response("User registered successfully")

    except EmailAlreadyRegisteredError as e:
        return error_response(str(e), status_code=409)


@router.post("/login")
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: Annotated[EmailLoginForm, Form()],
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service),
    log_publisher: LogPublisher = Depends(get_log_publisher),
) -> JSONResponse:
    """
    Basic auth with login and password
    """
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
        response = success_response(
            "Authenticated successfully", data={"user": token_data["user"]}
        )
        response.set_cookie(
            key="access_token",
            value=token_data["access_token"],
            httponly=True,
            secure=settings.secure_cookies,
            samesite="lax",
            max_age=settings.jwt_max_age_seconds,
        )
        return response

    except InvalidCredentialsError as e:
        return error_response(str(e), status_code=401)


@router.get("/google/init")
async def google_init(
    request: Request,
    provider: OAuthProvider = Depends(get_google_provider),
) -> RedirectResponse:
    """
    Initialize OAuth flow - redirect to Google OAuth page.
    After successful authorization, Google redirects to /api/v1/auth/google/callback
    """
    # Use fixed redirect_uri from settings
    callback_url = settings.GOOGLE_REDIRECT_URI

    if settings.ENVIRONMENT == "development":
        logger.debug(f"Google OAuth init - redirect_uri: {callback_url}")

    # Google OAuth URL
    google_oauth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.CLIENT_ID,
        "redirect_uri": callback_url,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    auth_url = f"{google_oauth_url}?{urlencode(params)}"
    logger.info("Redirecting to Google OAuth")

    return RedirectResponse(url=auth_url)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    code: str = Query(...),
    token_service: TokenService = Depends(get_token_service),
    provider: OAuthProvider = Depends(get_google_provider),
    user_repo: UserRepository = Depends(get_user_repository),
    oauth_repo: OAuthAccountRepository = Depends(get_oauth_account_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
) -> RedirectResponse:
    """
    Google OAuth callback endpoint.
    Exchanges authorization code for token, authenticates user, and redirects to SPA.
    """
    client_ip = request.client.host if request and request.client else "unknown"

    try:
        # Use the same redirect_uri as in initialization
        callback_url = settings.GOOGLE_REDIRECT_URI

        if settings.ENVIRONMENT == "development":
            logger.debug(f"Google OAuth callback - redirect_uri: {callback_url}")
        else:
            logger.info("Google OAuth callback received")

        token_data = await authenticate_oauth_user(
            code,
            provider,
            token_service,
            user_repo,
            oauth_repo,
            client_ip,
            log_publisher,
            redirect_uri=callback_url,
        )

        # Redirect to frontend after successful authentication
        redirect_url = f"{settings.FRONTEND_URL}/main"

        # Create redirect response with cookie
        response = RedirectResponse(url=redirect_url)
        response.set_cookie(
            key="access_token",
            value=token_data["access_token"],
            httponly=True,
            secure=settings.secure_cookies,
            samesite="Lax",
            max_age=settings.jwt_max_age_seconds,
        )

        return response

    except InvalidCredentialsError:
        # Redirect to login page with error
        error_url = f"{settings.FRONTEND_URL}/login?error=oauth_failed"
        return RedirectResponse(url=error_url)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: UserEntity = Depends(get_current_user)) -> UserOut:
    """
    Endpoint to receive information about the user
    """
    return UserOut(
        id=current_user.id.value,
        email=current_user.email.value,
        username=current_user.username.value if current_user.username else None,
        avatar_url=current_user.avatar_url.value if current_user.avatar_url else None,
    )


@router.post("/logout")
def logout(response: Response):
    """
    Logout endpoint
    """
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
