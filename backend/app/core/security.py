from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.interfaces import PasswordHasher, TokenService
from app.db.models.user import User
from app.db.session import get_db
from app.domain.value_objects.user import UserPasswordHash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class BcryptHasher(PasswordHasher):
    def hash(self, password: str) -> UserPasswordHash:
        return pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: UserPasswordHash) -> bool:
        return pwd_context.verify(plain_password, str(hashed_password))


class JWTTokenService(TokenService):
    def create_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user
