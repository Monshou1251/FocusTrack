from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.core.dependencies import get_journal_repository, get_log_publisher
from app.core.security.user_security import get_current_user
from app.domain.interfaces.journal_repository import IJournalRepository
from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.services.journal_service import (
    create_journal_entry_service,
    delete_journal_entry_service,
    get_journal_entries_service,
    get_journal_entry_service,
    search_journal_entries_service,
    update_journal_entry_service,
)

router = APIRouter()


class CreateJournalEntryModel(BaseModel):
    title: str
    content: str


class UpdateJournalEntryModel(BaseModel):
    title: str | None = None
    content: str | None = None


@router.get("/entries")
async def get_entries(
    request: Request,
    include_archived: bool = False,
    current_user=Depends(get_current_user),
    journal_repo: IJournalRepository = Depends(get_journal_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"
    entries = await get_journal_entries_service(
        journal_repo=journal_repo,
        user_id=current_user.id.value,
        include_archived=include_archived,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
    )
    return [
        {
            "id": e.id,
            "title": e.title,
            "content": e.content,
            "created_at": e.created_at,
            "user_id": e.user_id.value if hasattr(e.user_id, "value") else e.user_id,
        }
        for e in entries
    ]


@router.post("/entries")
async def create_entry(
    request: Request,
    data: CreateJournalEntryModel,
    current_user=Depends(get_current_user),
    journal_repo: IJournalRepository = Depends(get_journal_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"
    e = await create_journal_entry_service(
        journal_repo=journal_repo,
        user_id=current_user.id.value,
        title=data.title,
        content=data.content,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
    )
    return {
        "id": e.id,
        "title": e.title,
        "content": e.content,
        "created_at": e.created_at,
        "user_id": e.user_id.value if hasattr(e.user_id, "value") else e.user_id,
    }


@router.get("/entries/{entry_id}")
async def get_entry(
    request: Request,
    entry_id: int,
    current_user=Depends(get_current_user),
    journal_repo: IJournalRepository = Depends(get_journal_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"
    e = await get_journal_entry_service(
        journal_repo=journal_repo,
        entry_id=entry_id,
        user_id=current_user.id.value,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
    )
    if e is None:
        return None
    return {
        "id": e.id,
        "title": e.title,
        "content": e.content,
        "created_at": e.created_at,
        "user_id": e.user_id.value if hasattr(e.user_id, "value") else e.user_id,
    }


@router.put("/entries/{entry_id}")
async def update_entry(
    request: Request,
    entry_id: int,
    data: UpdateJournalEntryModel,
    current_user=Depends(get_current_user),
    journal_repo: IJournalRepository = Depends(get_journal_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"
    e = await update_journal_entry_service(
        journal_repo=journal_repo,
        entry_id=entry_id,
        user_id=current_user.id.value,
        title=data.title,
        content=data.content,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
    )
    return {
        "id": e.id,
        "title": e.title,
        "content": e.content,
        "created_at": e.created_at,
        "user_id": e.user_id.value if hasattr(e.user_id, "value") else e.user_id,
    }


@router.delete("/entries/{entry_id}")
async def delete_entry(
    request: Request,
    entry_id: int,
    current_user=Depends(get_current_user),
    journal_repo: IJournalRepository = Depends(get_journal_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"
    return await delete_journal_entry_service(
        journal_repo=journal_repo,
        entry_id=entry_id,
        user_id=current_user.id.value,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
    )


@router.get("/search")
async def search_entries(
    request: Request,
    q: str,
    include_archived: bool = False,
    current_user=Depends(get_current_user),
    journal_repo: IJournalRepository = Depends(get_journal_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"
    entries = await search_journal_entries_service(
        journal_repo=journal_repo,
        user_id=current_user.id.value,
        query=q,
        include_archived=include_archived,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
    )
    return [
        {
            "id": e.id,
            "title": e.title,
            "content": e.content,
            "created_at": e.created_at,
            "user_id": e.user_id.value if hasattr(e.user_id, "value") else e.user_id,
        }
        for e in entries
    ]
