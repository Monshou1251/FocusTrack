from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category
from app.db.models.sprint import Sprint as ORMSprint
from app.domain.entities.sprint import Sprint as EntitySprint
from app.domain.interfaces.sprint_repository import ISprintRepository
from app.infrastructure.sqla_persistence.mappings.sprint_mapping import (
    sprint_orm_to_entity,
)


class SQLAlchemySprintRepository(ISprintRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_sprint_to_db(
        self, user_id: int, category_id: int, duration: int, started_at: datetime
    ) -> EntitySprint:
        sprint = ORMSprint(
            user_id=user_id,
            category_id=category_id,
            duration=duration,
            started_at=started_at,
        )

        self.session.add(sprint)
        await self.session.commit()

        await self.session.refresh(sprint, ["user", "category"])

        return sprint_orm_to_entity(sprint)

    async def get_category_id_by_name(self, user_id: int, category_name: str) -> int:
        stmt = select(Category.id).where(
            Category.user_id == user_id, Category.name == category_name
        )
        result = await self.session.execute(stmt)
        category_id = result.scalar_one_or_none()

        if category_id is None:
            raise ValueError(
                f"No category named '{category_name}' was found for user_id = {user_id}"
            )

        return category_id
