from app.db.models.user import User as ORMUser
from app.domain.entities.user import User as EntityUser
from app.domain.value_objects.user import Email, UserId, Username, UserPasswordHash


def user_orm_to_entity(orm_user: ORMUser) -> EntityUser:
    return EntityUser(
        id_=UserId(orm_user.id),
        username=Username(orm_user.username),
        email=Email(orm_user.email),
        hashed_password=UserPasswordHash(orm_user.hashed_password),
        role=orm_user.role,
        auth_provider=orm_user.auth_provider,
    )


def user_entity_to_orm(entity: EntityUser) -> ORMUser:
    return ORMUser(
        id=entity.id_.value,
        username=entity.username.value,
        email=entity.email.value,
        hashed_password=entity.hashed_password.value,
        role=entity.role,
        auth_provider=entity.auth_provider,
    )
