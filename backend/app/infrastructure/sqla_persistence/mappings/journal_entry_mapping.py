from app.db.models.journal import JournalEntry as ORMJournalEntry
from app.domain.entities.journal import JournalEntry as EntityJournalEntry


def orm_to_entity(orm_obj: ORMJournalEntry) -> EntityJournalEntry:
    return EntityJournalEntry(
        id_=orm_obj.id,
        user_id=orm_obj.user_id,
        title=orm_obj.title,
        content=orm_obj.content,
        created_at=orm_obj.created_at,
    )


def entity_to_orm(entity: EntityJournalEntry) -> ORMJournalEntry:
    return ORMJournalEntry(
        id=entity.id,
        user_id=entity.user_id,
        title=entity.title,
        content=entity.content,
        created_at=entity.created_at,
    )
