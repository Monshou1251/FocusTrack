from dataclasses import dataclass

from app.domain.entities.base import Entity
from app.domain.enums.user_role import UserRole
from app.domain.value_objects.user import (
    AvatarUrl,
    Email,
    UserId,
    Username,
    UserPasswordHash,
)


@dataclass(eq=False, kw_only=True)
class User(Entity[UserId]):
    username: Username
    email: Email
    hashed_password: UserPasswordHash
    role: UserRole
    auth_provider: str
    avatar_url: AvatarUrl
