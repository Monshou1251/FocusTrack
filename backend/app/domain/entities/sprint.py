from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import Entity
from app.domain.value_objects.user import (
    Email,
    UserId,
)


@dataclass(eq=False, kw_only=True)
class Sprint(Entity[UserId]):
    email: Email
    category: str
    duration: int
    started_at: datetime
