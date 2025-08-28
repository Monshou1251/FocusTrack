from datetime import UTC, datetime

from app.domain.entities.journal import JournalEntry
from app.domain.interfaces.journal_repository import IJournalRepository
from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.services.logging_service import log_journal_operation_attempt
from app.domain.value_objects.user import UserId


async def create_journal_entry_service(
    journal_repo: IJournalRepository,
    user_id: int,
    title: str,
    content: str,
    email: str = "",
    client_ip: str = "",
    log_publisher: LogPublisher = None,
) -> JournalEntry:
    try:
        journal_entry = JournalEntry(
            id_=0,
            title=title,
            content=content,
            user_id=UserId(user_id),
            created_at=datetime.now(UTC),
        )

        created_entry = await journal_repo.create_journal_entry(journal_entry)

        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="create_journal_entry",
                user_id=user_id,
                email=email,
                entry_id=created_entry.id,
                ip=client_ip,
                success=True,
                extra={"title": title, "content_length": len(content)},
            )

        return created_entry
    except Exception as e:
        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="create_journal_entry",
                user_id=user_id,
                email=email,
                entry_id=None,
                ip=client_ip,
                success=False,
                error=str(e),
            )
        raise


async def get_journal_entries_service(
    journal_repo: IJournalRepository,
    user_id: int,
    include_archived: bool = False,
    email: str = "",
    client_ip: str = "",
    log_publisher: LogPublisher = None,
) -> list[JournalEntry]:
    try:
        entries = await journal_repo.get_journal_entries_by_user_id(
            user_id, include_archived
        )

        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="get_journal_entries",
                user_id=user_id,
                email=email,
                entry_id=None,
                ip=client_ip,
                success=True,
                extra={
                    "entries_count": len(entries),
                    "include_archived": include_archived,
                },
            )

        return entries
    except Exception as e:
        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="get_journal_entries",
                user_id=user_id,
                email=email,
                entry_id=None,
                ip=client_ip,
                success=False,
                error=str(e),
            )
        raise


async def get_journal_entry_service(
    journal_repo: IJournalRepository,
    entry_id: int,
    user_id: int,
    email: str = "",
    client_ip: str = "",
    log_publisher: LogPublisher = None,
) -> JournalEntry | None:
    try:
        entry = await journal_repo.get_journal_entry_by_id(entry_id, user_id)

        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="get_journal_entry",
                user_id=user_id,
                email=email,
                entry_id=entry_id,
                ip=client_ip,
                success=entry is not None,
                extra={"found": entry is not None},
            )

        return entry
    except Exception as e:
        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="get_journal_entry",
                user_id=user_id,
                email=email,
                entry_id=entry_id,
                ip=client_ip,
                success=False,
                error=str(e),
            )
        raise


async def update_journal_entry_service(
    journal_repo: IJournalRepository,
    entry_id: int,
    user_id: int,
    title: str | None = None,
    content: str | None = None,
    email: str = "",
    client_ip: str = "",
    log_publisher: LogPublisher = None,
) -> JournalEntry:
    try:
        existing_entry = await journal_repo.get_journal_entry_by_id(entry_id, user_id)
        if not existing_entry:
            raise ValueError("Journal entry not found")

        if title is not None:
            existing_entry.title = title
        if content is not None:
            existing_entry.content = content

        updated_entry = await journal_repo.update_journal_entry(existing_entry)

        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="update_journal_entry",
                user_id=user_id,
                email=email,
                entry_id=entry_id,
                ip=client_ip,
                success=True,
                extra={
                    "updated_fields": [
                        k
                        for k, v in locals().items()
                        if v is not None
                        and k
                        not in [
                            "journal_repo",
                            "entry_id",
                            "user_id",
                            "email",
                            "client_ip",
                            "log_publisher",
                        ]
                    ]
                },
            )

        return updated_entry
    except Exception as e:
        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="update_journal_entry",
                user_id=user_id,
                email=email,
                entry_id=entry_id,
                ip=client_ip,
                success=False,
                error=str(e),
            )
        raise


async def delete_journal_entry_service(
    journal_repo: IJournalRepository,
    entry_id: int,
    user_id: int,
    email: str = "",
    client_ip: str = "",
    log_publisher: LogPublisher = None,
) -> bool:
    try:
        success = await journal_repo.delete_journal_entry(entry_id, user_id)

        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="delete_journal_entry",
                user_id=user_id,
                email=email,
                entry_id=entry_id,
                ip=client_ip,
                success=success,
                extra={"deleted": success},
            )

        return success
    except Exception as e:
        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="delete_journal_entry",
                user_id=user_id,
                email=email,
                entry_id=entry_id,
                ip=client_ip,
                success=False,
                error=str(e),
            )
        raise


async def search_journal_entries_service(
    journal_repo: IJournalRepository,
    user_id: int,
    query: str,
    include_archived: bool = False,
    email: str = "",
    client_ip: str = "",
    log_publisher: LogPublisher = None,
) -> list[JournalEntry]:
    try:
        entries = await journal_repo.search_journal_entries(
            user_id, query, include_archived
        )

        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="search_journal_entries",
                user_id=user_id,
                email=email,
                entry_id=None,
                ip=client_ip,
                success=True,
                extra={
                    "query": query,
                    "results_count": len(entries),
                    "include_archived": include_archived,
                },
            )

        return entries
    except Exception as e:
        if log_publisher:
            await log_journal_operation_attempt(
                log_publisher=log_publisher,
                event="search_journal_entries",
                user_id=user_id,
                email=email,
                entry_id=None,
                ip=client_ip,
                success=False,
                error=str(e),
            )
        raise
