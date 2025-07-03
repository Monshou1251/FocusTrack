from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import Entity
from app.domain.value_objects.category import CategoryId, CategoryName
from app.domain.value_objects.user import UserId


@dataclass(eq=False, kw_only=True)
class Category(Entity[CategoryId]):
    name: CategoryName
    created_at: datetime
    user_id: UserId
