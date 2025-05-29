from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User, OAuthAccount
from app.core.interfaces import UserRepository
from typing import Optional


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        
        return result.scalars().first()
    
    
    async def create_user(self, email: str, hashed_password: str, auth_provider: str = "email") -> User:
        user = User(email=email, hashed_password=hashed_password, auth_provider=auth_provider)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user

    async def get_user_by_oauth(self, provider: str, provider_id: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .join(OAuthAccount)
            .where(OAuthAccount.provider == provider, OAuthAccount.provider_id == provider_id)
        )
        
        return result.scalars().first()
    
    async def create_oauth_user(self, email: str, auth_provider: str) -> User:
        user = User(email=email, hashed_password=None, auth_provider=auth_provider)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def create_oauth_account(self, provider: str, provider_id: str, user: User) -> User:
        oauth_account = OAuthAccount(
            provider=provider,
            provider_id=provider_id,
            user_id=user.id,
        )
        self.db.add(oauth_account)
        await self.db.commit()
        await self.db.refresh(user)
        return user
