from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category as ORMCategory
from app.domain.entities.category import Category as EntityCategory
from app.domain.interfaces.category_repository import ICategoryRepository
from app.infrastructure.sqla_persistence.mappings.category_mapping import (
    category_orm_to_entity,
)


class SQLAlchemyCategoryRepository(ICategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_categories_from_db(self, user_id: int) -> list[dict[str, str]]:
        stmt = select(ORMCategory.id, ORMCategory.name).where(
            ORMCategory.user_id == user_id
        )
        result = await self.session.execute(stmt)
        categories = [{"id": row.id, "name": row.name} for row in result.all()]

        return categories

    async def save_category_to_db(
        self, user_id: int, name: str, created_at: datetime
    ) -> EntityCategory:
        category = ORMCategory(
            user_id=user_id,
            name=name,
            created_at=created_at,
        )

        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)

        return category_orm_to_entity(category)

    async def update_category_in_db(
        self, user_id: int, category_id: int, name: str
    ) -> EntityCategory:
        # First find the existing category
        stmt = select(ORMCategory).where(
            ORMCategory.id == category_id, ORMCategory.user_id == user_id
        )
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()

        if not category:
            raise ValueError(
                f"Category with id {category_id} not found for user {user_id}"
            )

        # Update the name
        category.name = name
        await self.session.commit()
        await self.session.refresh(category)

        return category_orm_to_entity(category)

    async def delete_category_from_db(self, user_id: int, category_id: int):
        # First find the existing category
        stmt = select(ORMCategory).where(
            ORMCategory.id == category_id, ORMCategory.user_id == user_id
        )
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()

        if not category:
            raise ValueError(
                f"Category with id {category_id} not found for user {user_id}"
            )

        # Convert to entity before deletion
        category_entity = category_orm_to_entity(category)

        await self.session.delete(category)
        await self.session.commit()

        return category_entity
