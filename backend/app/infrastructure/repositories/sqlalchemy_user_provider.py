from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import OAuthAccount
from app.db.models.user import User as ORMUser
from app.domain.entities.user import User as EntityUser
from app.domain.interfaces.oauth_account_repository import OAuthAccountRepository
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.sqla_persistence.mappings.user_mapping import (
    user_orm_to_entity,
)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> EntityUser | None:
        result = await self.session.execute(
            select(ORMUser).where(ORMUser.email == email)
        )
        orm_user = result.scalar_one_or_none()

        return user_orm_to_entity(orm_user) if orm_user else None

    async def create_user(
        self, email: str, hashed_password: str, auth_provider: str = "email"
    ) -> EntityUser:
        orm_user = ORMUser(
            email=email,
            hashed_password=hashed_password,
            auth_provider=auth_provider,
            username=email.split("@")[0],
        )
        self.session.add(orm_user)
        await self.session.commit()
        await self.session.refresh(orm_user)
        return user_orm_to_entity(orm_user)


class SQLAlchemyOAuthAccountRepository(OAuthAccountRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_oauth(
        self, provider: str, provider_id: str
    ) -> EntityUser | None:
        # Найдём OAuthAccount с таким провайдером и ID
        stmt = (
            select(ORMUser)
            .join(OAuthAccount, ORMUser.id == OAuthAccount.user_id)
            .where(
                OAuthAccount.provider == provider,
                OAuthAccount.provider_id == provider_id,
            )
        )
        result = await self.session.execute(stmt)
        orm_user = result.scalars().first()
        if orm_user is None:
            return None
        return user_orm_to_entity(orm_user)

    async def create_oauth_user(
        self,
        email: str,
        auth_provider: str,
        avatar_url: str | None = None,
    ) -> EntityUser:
        user = ORMUser(
            email=email,
            hashed_password=None,
            auth_provider=auth_provider,
            username=email.split("@")[0],
            avatar_url=avatar_url,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user_orm_to_entity(user)

    async def create_oauth_account(
        self,
        provider: str,
        provider_id: str,
        user: EntityUser,
    ) -> EntityUser:
        print("user: ", user)
        oauth_account = OAuthAccount(
            provider=provider,
            provider_id=provider_id,
            user_id=user.id_.value,
        )
        self.session.add(oauth_account)
        await self.session.commit()

        # Получаем ORMUser по user_id
        stmt = select(ORMUser).where(ORMUser.id == user.id_.value)
        result = await self.session.execute(stmt)
        orm_user = result.scalar_one()

        return user_orm_to_entity(orm_user)
