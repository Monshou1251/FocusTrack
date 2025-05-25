from app.core.interfaces import PasswordHasher, TokenService, OAuthProvider
from app.core.security import BcryptHasher, JWTTokenService
from app.infrastructure.oauth_providers.google_provider import GoogleOAuthProvider


def get_password_hasher() -> PasswordHasher:
    return BcryptHasher()

def get_token_service() -> TokenService:
    return JWTTokenService()

def get_google_provider() -> OAuthProvider:
    return GoogleOAuthProvider()
