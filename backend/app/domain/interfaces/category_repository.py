from datetime import datetime
from typing import Protocol

from app.domain.entities.category import Category


class ICategoryRepository(Protocol):
    async def get_categories_from_db(self, user_id: int) -> list[dict[str, str]]: ...

    async def save_category_to_db(
        self,
        user_id: int,
        name: str,
        created_at: datetime,
    ) -> Category: ...

    async def update_category_in_db(
        self,
        user_id: int,
        category_id: int,
        name: str,
    ) -> Category: ...

    async def delete_category_from_db(
        self,
        user_id: int,
        category_id: int,
    ) -> Category: ...
