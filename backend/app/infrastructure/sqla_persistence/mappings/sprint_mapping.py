from app.db.models.sprint import Sprint as ORMSprint
from app.domain.entities.sprint import Sprint as EntitySprint
from app.domain.entities.user import User as EntityUser
from app.domain.value_objects.user import Email, UserId


def sprint_orm_to_entity(orm_sprint: ORMSprint) -> EntitySprint:
    return EntitySprint(
        id_=UserId(orm_sprint.user_id),
        email=Email(orm_sprint.user.email),
        category=orm_sprint.category.name,
        duration=orm_sprint.duration,
        started_at=orm_sprint.started_at,
    )


def user_entity_to_orm(entity: EntityUser) -> ORMSprint:
    return ORMSprint(
        id=entity.id_.value,
        username=entity.username.value,
        email=entity.email.value,
        hashed_password=entity.hashed_password.value,
        role=entity.role,
        auth_provider=entity.auth_provider,
        avatar_url=entity.avatar_url,
    )
