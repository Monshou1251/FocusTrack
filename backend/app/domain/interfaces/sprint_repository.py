from datetime import datetime
from typing import Protocol

from app.domain.entities.sprint import Sprint


class ISprintRepository(Protocol):
    async def save_sprint_to_db(
        self,
        user_id: int,
        category_id: int,
        duration: int,
        started_at: datetime,
    ) -> Sprint: ...

    async def get_category_id_by_name(
        self, user_id: int, category_name: str
    ) -> int: ...
