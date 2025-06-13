import asyncio

from fastapi.security import OAuth2PasswordBearer

from app.core.interfaces import (
    LogPublisher,
    OAuthAccountRepository,
    OAuthProvider,
    PasswordHasher,
    TokenService,
    UserRepository,
)
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.domain.services.logging_service import (
    log_auth_attempt,
    log_oauth_attempt,
    log_registration_attempt,
)
from app.schemas.auth import EmailLoginForm, EmailRegisterForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def register_user(
    form_data: EmailRegisterForm,
    user_repo: UserRepository,
    hasher: PasswordHasher,
    client_ip: str,
    log_publisher: LogPublisher,
):
    email = form_data.email
    password = form_data.password

    error_message = None
    success = False
    try:
        if not email or not password:
            error_message = "Please provide email and password"
            raise EmailAlreadyRegisteredError(error_message)

        existing_user = await user_repo.get_user_by_email(email)

        if existing_user:
            if existing_user.auth_provider != "email":
                error_message = "Email already registered through OAuth"
            else:
                error_message = "Email already registered"

            raise EmailAlreadyRegisteredError(error_message)

        hashed_password = hasher.hash(password)
        await user_repo.create_user(email, hashed_password, auth_provider="email")
        success = True

    finally:
        asyncio.create_task(
            log_registration_attempt(
                log_publisher=log_publisher,
                email=form_data.email,
                success=success,
                ip=client_ip,
                error=error_message,
            )
        )


async def authenticate_user(
    form_data: EmailLoginForm,
    user_repo: UserRepository,
    hasher: PasswordHasher,
    token_service: TokenService,
    client_ip: str,
    log_publisher: LogPublisher,
):
    user = await user_repo.get_user_by_email(form_data.email)

    success = False
    token = None
    error_message = None

    if user and hasher.verify(form_data.password, user.hashed_password):
        success = True
        token = token_service.create_token({"sub": str(user.email)})
    else:
        error_message = "Incorrect email or password"

    asyncio.create_task(
        log_auth_attempt(
            log_publisher=log_publisher,
            email=form_data.email,
            success=success,
            ip=client_ip,
            error=error_message,
        )
    )

    if not success:
        raise InvalidCredentialsError()

    return {"access_token": token, "token_type": "bearer"}


async def authenticate_oauth_user(
    code: str,
    oauth_provider: OAuthProvider,
    token_service: TokenService,
    user_repo: UserRepository,
    oauth_repo: OAuthAccountRepository,
    client_ip: str,
    log_publisher: LogPublisher,
) -> dict:
    success = False
    error = None
    user_email = "unknown"

    try:
        token_data = await oauth_provider.exchange_code_for_token(code)
        access_token = token_data["access_token"]
        user_info = await oauth_provider.get_user_info(access_token)
        user_email = user_info.get("email", "unknown")

        if "id" not in user_info or "email" not in user_info:
            error = "Invalid user info from OAuth provider"
            raise InvalidCredentialsError()

        user = await oauth_repo.get_user_by_oauth(oauth_provider.name, user_info["id"])
        if not user:
            user = await user_repo.get_user_by_email(user_info["email"])
            if not user:
                user = await oauth_repo.create_oauth_user(
                    user_info["email"],
                    auth_provider=oauth_provider.name,
                    avatar_url=user_info.get("picture"),
                )
                if not user:
                    raise RuntimeError("User creation failed")

            await oauth_repo.create_oauth_account(
                provider=oauth_provider.name,
                provider_id=user_info["id"],
                user=user,
            )

        token = token_service.create_token({"sub": str(user.email)})
        success = True

    except Exception as err:
        error = error or "OAuth authentication failed"
        raise InvalidCredentialsError() from err

    finally:
        asyncio.create_task(
            log_oauth_attempt(
                log_publisher=log_publisher,
                email=user_email,
                success=success,
                ip=client_ip,
                error=error,
            )
        )

    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token):
    pass
