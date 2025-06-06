from dataclasses import dataclass

from app.domain.entities.base import Entity
from app.domain.enums.user_role import UserRole
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.user_password_hash import UserPasswordHash
from app.domain.value_objects.username import Username


@dataclass(eq=False, kw_only=True)
class User(Entity[UserId]):
    username: Username
    email: Email
    password_hash: UserPasswordHash
    role: UserRole
    auth_provider: str
