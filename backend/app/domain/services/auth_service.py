from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import EmailLoginForm, EmailRegisterForm
from app.core.interfaces import PasswordHasher, TokenService, OAuthProvider, UserRepository, LogPublisher
from app.core.responses import success_response, error_response
from app.domain.exceptions.auth_exceptions import InvalidCredentialsError, EmailAlreadyRegisteredError
from datetime import datetime, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login') 


async def register_user(
    form_data: EmailRegisterForm,
    user_repo: UserRepository,
    hasher: PasswordHasher,
    client_ip: str,
    log_publisher: LogPublisher
):
    email = form_data.email
    password = form_data.password
    print(email)
    print(password)
    
    error_message = None
    success = False

    if not email or not password:
        error_message = "Please provide email and password"
        raise EmailAlreadyRegisteredError(error_message) 
    
    existing_user = await user_repo.get_user_by_email(email)

    if existing_user:
        if existing_user.auth_provider != 'email':
            error_message = "Email already registered through OAuth"
        else:
            error_message = "Email already registered"

        await log_publisher.publish({
            "event": "user_register_attempt",
            "email": email,
            "success": success,
            "ip": client_ip,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": error_message
        })

        raise EmailAlreadyRegisteredError(error_message)

    hashed_password = hasher.hash(password)
    await user_repo.create_user(email, hashed_password, auth_provider="email")
    success = True

    await log_publisher.publish({
        "event": "user_register_attempt",
        "email": email,
        "success": success,
        "ip": client_ip,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": None
    })



async def authenticate_user(
    form_data: EmailLoginForm,
    user_repo: UserRepository,
    hasher: PasswordHasher,
    token_service: TokenService,
    client_ip: str,
    log_publisher: LogPublisher
):
    user = await user_repo.get_user_by_email(form_data.email)

    success = False
    token = None
    error_message = None

    if user and hasher.verify(form_data.password, user.hashed_password):
        success = True
        token = token_service.create_token({"sub": user.email})
    else:
        error_message = "Incorrect email or password"

    await log_publisher.publish({
        "event": "user_login_attempt",
        "email": form_data.email,
        "success": success,
        "ip": client_ip,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": error_message
    })

    if not success:
        raise InvalidCredentialsError()

    return {
        "access_token": token,
        "token_type": "bearer"
    }



async def oauth_login(
    code: str,
    oauth_provider: OAuthProvider,
    token_service: TokenService,
    user_repo: UserRepository,
):
    try:
        token_data = await oauth_provider.exchange_code_for_token(code)
        access_token = token_data["access_token"]
        user_info = await oauth_provider.get_user_info(access_token)
    except Exception:
        return error_response("OAuth authentication failed", status_code=400)

    if "id" not in user_info or "email" not in user_info:
        return error_response("Invalid user info from OAuth provider", status_code=400)

    user = await user_repo.get_user_by_oauth(oauth_provider.name, user_info["id"])
    if not user:
        user = await user_repo.get_user_by_email(user_info["email"])
        if not user:
            user = await user_repo.create_oauth_user(
                user_info["email"],
                auth_provider=oauth_provider.name,
            )
        await user_repo.create_oauth_account(
            provider=oauth_provider.name,
            provider_id=user_info["id"],
            user=user,
        )

    token = token_service.create_token({"sub": user.email})
    return success_response("Authenticated via OAuth", data={"access_token": token, "token_type": "bearer"})





async def get_current_user(token):
    pass
