from app.db.models.user import OAuthAccount as ORMOAuthAccount
from app.db.models.user import User as ORMUser
from app.domain.entities.oauth_user import OAuthAccount as EntityOAuthAccount
from app.domain.value_objects.oauth import OAuthProvider, ProviderId, UserId


def user_orm_to_entity_oauth(orm_account: ORMOAuthAccount) -> EntityOAuthAccount:
    return EntityOAuthAccount(
        id_=orm_account.id,
        provider=OAuthProvider(orm_account.provider),
        provider_id=ProviderId(orm_account.provider_id),
        user_id=UserId(orm_account.user_id),
    )


def user_entity_to_orm_oauth(entity: ORMUser) -> ORMOAuthAccount:
    return ORMOAuthAccount(
        id=entity.id_,
        provider=entity.provider.value,
        provider_id=entity.provider_id.value,
        user_id=entity.user_id.value,
    )
