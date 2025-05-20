from app.core.interfaces import PasswordHasher, TokenService
from app.core.security import BcryptHasher, JWTTokenService  


def get_password_hasher() -> PasswordHasher:
    return BcryptHasher()

def get_token_service() -> TokenService:
    return JWTTokenService()
