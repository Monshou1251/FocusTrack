from abc import ABC, abstractmethod

from app.domain.entities.journal import JournalEntry


class IJournalRepository(ABC):
    @abstractmethod
    async def create_journal_entry(self, journal_entry: JournalEntry) -> JournalEntry:
        pass

    @abstractmethod
    async def get_journal_entry_by_id(
        self, entry_id: int, user_id: int
    ) -> JournalEntry | None:
        pass

    @abstractmethod
    async def get_journal_entries_by_user_id(
        self, user_id: int, include_archived: bool = False
    ) -> list[JournalEntry]:
        pass

    @abstractmethod
    async def update_journal_entry(self, journal_entry: JournalEntry) -> JournalEntry:
        pass

    @abstractmethod
    async def delete_journal_entry(self, entry_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    async def search_journal_entries(
        self, user_id: int, query: str, include_archived: bool = False
    ) -> list[JournalEntry]:
        pass
