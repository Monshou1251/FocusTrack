from datetime import UTC, datetime

from app.domain.interfaces.category_repository import ICategoryRepository
from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.services.logging_service import (
    log_category_operation_attempt,
)


async def get_category_service(
    category_repo: ICategoryRepository,
    user_id: int,
    email: str,
    client_ip: str,
    log_publisher: LogPublisher,
):
    try:
        categories = await category_repo.get_categories_from_db(user_id)

        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="get_categories",
            user_id=user_id,
            email=email,
            category_id=None,
            category_name=None,
            ip=client_ip,
            success=True,
            extra={"categories_count": len(categories)},
        )

        return {"categories": categories}

    except Exception as e:
        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="get_categories",
            user_id=user_id,
            email=email,
            category_id=None,
            category_name=None,
            ip=client_ip,
            success=False,
            error=str(e),
        )
        raise


async def create_category_service(
    category_repo: ICategoryRepository,
    user_id: int,
    email: str,
    client_ip: str,
    log_publisher: LogPublisher,
    name: str,
):
    try:
        created_at = datetime.now(UTC)

        category = await category_repo.save_category_to_db(
            user_id=user_id,
            name=name,
            created_at=created_at,
        )

        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="create_category",
            user_id=user_id,
            email=email,
            category_id=category.id.value,
            category_name=name,
            ip=client_ip,
            success=True,
            extra={"category_name": name},
        )

        return category

    except Exception as e:
        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="create_category",
            user_id=user_id,
            email=email,
            category_id=None,
            category_name=name,
            ip=client_ip,
            success=False,
            error=str(e),
        )
        raise


async def delete_category_service(
    category_repo: ICategoryRepository,
    user_id: int,
    email: str,
    client_ip: str,
    log_publisher: LogPublisher,
    category_id: int,
):
    try:
        deleted_category = await category_repo.delete_category_from_db(
            user_id=user_id,
            category_id=category_id,
        )

        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="delete_category",
            user_id=user_id,
            email=email,
            category_id=category_id,
            category_name=deleted_category.name.value,
            ip=client_ip,
            success=True,
            extra={"deleted_category_id": category_id},
        )

    except Exception as e:
        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="delete_category",
            user_id=user_id,
            email=email,
            category_id=category_id,
            category_name=None,
            ip=client_ip,
            success=False,
            error=str(e),
        )
        raise


async def update_category_service(
    category_repo: ICategoryRepository,
    user_id: int,
    email: str,
    client_ip: str,
    log_publisher: LogPublisher,
    category_id: int,
    name: str,
):
    try:
        updated_category = await category_repo.update_category_in_db(
            user_id=user_id,
            category_id=category_id,
            name=name,
        )

        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="update_category",
            user_id=user_id,
            email=email,
            category_id=category_id,
            category_name=name,
            ip=client_ip,
            success=True,
            extra={"updated_category_name": name},
        )

        return updated_category

    except Exception as e:
        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="update_category",
            user_id=user_id,
            email=email,
            category_id=category_id,
            category_name=name,
            ip=client_ip,
            success=False,
            error=str(e),
        )
        raise
