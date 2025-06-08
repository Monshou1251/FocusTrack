from dataclasses import dataclass

from app.domain.entities.base import Entity
from app.domain.value_objects.oauth import OAuthProvider, ProviderId, UserId


@dataclass(eq=False, kw_only=True)
class OAuthAccount(Entity[UserId]):
    provider: OAuthProvider
    provider_id: ProviderId
    user_id: UserId
