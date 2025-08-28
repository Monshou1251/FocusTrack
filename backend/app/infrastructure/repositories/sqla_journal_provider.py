from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.journal import JournalEntry as ORMJournalEntry
from app.domain.entities.journal import JournalEntry as EntityJournalEntry
from app.domain.interfaces.journal_repository import IJournalRepository
from app.infrastructure.sqla_persistence.mappings.journal_entry_mapping import (
    orm_to_entity,
)


class SQLAlchemyJournalRepository(IJournalRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_journal_entry(
        self, journal_entry: EntityJournalEntry
    ) -> EntityJournalEntry:
        orm_entry = ORMJournalEntry(
            user_id=(
                journal_entry.user_id.value
                if hasattr(journal_entry.user_id, "value")
                else journal_entry.user_id
            ),
            title=journal_entry.title,
            content=journal_entry.content,
            created_at=journal_entry.created_at or datetime.now(UTC),
        )
        self.session.add(orm_entry)
        await self.session.commit()
        await self.session.refresh(orm_entry)
        return orm_to_entity(orm_entry)

    async def get_journal_entry_by_id(
        self, entry_id: int, user_id: int
    ) -> EntityJournalEntry | None:
        stmt = select(ORMJournalEntry).where(
            ORMJournalEntry.id == entry_id,
            ORMJournalEntry.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        orm_entry = result.scalar_one_or_none()
        if orm_entry is None:
            return None
        return orm_to_entity(orm_entry)

    async def get_journal_entries_by_user_id(
        self, user_id: int, include_archived: bool = False
    ) -> list[EntityJournalEntry]:
        stmt = select(ORMJournalEntry).where(ORMJournalEntry.user_id == user_id)

        result = await self.session.execute(stmt)
        entries = result.scalars().all()
        return [orm_to_entity(e) for e in entries]

    async def update_journal_entry(
        self, journal_entry: EntityJournalEntry
    ) -> EntityJournalEntry:
        stmt = select(ORMJournalEntry).where(
            ORMJournalEntry.id == journal_entry.id,
            ORMJournalEntry.user_id == journal_entry.user_id,
        )
        result = await self.session.execute(stmt)
        orm_entry = result.scalar_one_or_none()
        if orm_entry is None:
            raise ValueError(
                f"Journal entry with id {journal_entry.id} \
                not found for user {journal_entry.user_id}"
            )

        orm_entry.title = journal_entry.title
        orm_entry.content = journal_entry.content

        await self.session.commit()
        await self.session.refresh(orm_entry)
        return orm_to_entity(orm_entry)

    async def delete_journal_entry(self, entry_id: int, user_id: int) -> bool:
        stmt = select(ORMJournalEntry).where(
            ORMJournalEntry.id == entry_id,
            ORMJournalEntry.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        orm_entry = result.scalar_one_or_none()
        if orm_entry is None:
            return False
        await self.session.delete(orm_entry)
        await self.session.commit()
        return True

    async def search_journal_entries(
        self, user_id: int, query: str, include_archived: bool = False
    ) -> list[EntityJournalEntry]:
        stmt = select(ORMJournalEntry).where(
            ORMJournalEntry.user_id == user_id,
            (ORMJournalEntry.title.ilike(f"%{query}%"))
            | (ORMJournalEntry.content.ilike(f"%{query}%")),
        )

        result = await self.session.execute(stmt)
        entries = result.scalars().all()
        return [orm_to_entity(e) for e in entries]
