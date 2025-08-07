from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.dependencies import get_token_service, get_user_repository
from app.domain.entities.user import User
from app.domain.interfaces.token_service import TokenService
from app.domain.interfaces.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    access_token: str = Cookie(None),
    user_repo: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated!")

    try:
        payload = token_service.verify_token(access_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")

    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    user = await user_repo.get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
