from fastapi import APIRouter, Depends, Request

from app.core.dependencies import (
    get_category_repository,
    get_log_publisher,
)
from app.core.security.user_security import get_current_user
from app.domain.entities.user import User as UserEntity
from app.domain.interfaces.category_repository import ICategoryRepository
from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.services.category_service import (
    create_category_service,
    delete_category_service,
    get_category_service,
    update_category_service,
)
from app.schemas.category import (
    CreateCategoryRequest,
    CreateCategoryResponse,
    UpdateCategoryRequest,
    UpdateCategoryResponse,
)

router = APIRouter()


@router.get("/categories")
async def get_categories(
    request: Request,
    current_user: UserEntity = Depends(get_current_user),
    category_repo: ICategoryRepository = Depends(get_category_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"

    return await get_category_service(
        category_repo=category_repo,
        user_id=current_user.id.value,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
    )


@router.post("/", response_model=CreateCategoryResponse)
async def create_category(
    request: Request,
    category_data: CreateCategoryRequest,
    current_user: UserEntity = Depends(get_current_user),
    category_repo: ICategoryRepository = Depends(get_category_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"

    category = await create_category_service(
        category_repo=category_repo,
        user_id=current_user.id.value,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
        name=category_data.name,
    )

    return CreateCategoryResponse(
        id=category.id.value,
        name=category.name.value,
        created_at=category.created_at,
    )


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    request: Request,
    current_user: UserEntity = Depends(get_current_user),
    category_repo: ICategoryRepository = Depends(get_category_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"

    await delete_category_service(
        category_repo=category_repo,
        user_id=current_user.id.value,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
        category_id=category_id,
    )

    return {"message": "Category deleted successfully"}


@router.patch("/{category_id}", response_model=UpdateCategoryResponse)
async def update_category(
    category_id: int,
    request: Request,
    category_data: UpdateCategoryRequest,
    current_user: UserEntity = Depends(get_current_user),
    category_repo: ICategoryRepository = Depends(get_category_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"

    category = await update_category_service(
        category_repo=category_repo,
        user_id=current_user.id.value,
        email=current_user.email.value,
        client_ip=client_ip,
        log_publisher=log_publisher,
        category_id=category_id,
        name=category_data.name,
    )

    return UpdateCategoryResponse(
        id=category.id.value,
        name=category.name.value,
        created_at=category.created_at,
    )
