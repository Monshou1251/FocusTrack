import asyncio

from app.domain.dto.sprint_dto import SprintSaveDTO
from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.interfaces.sprint_repository import ISprintRepository
from app.domain.services.logging_service import log_save_sprint_attempt


async def save_sprint_service(
    data: SprintSaveDTO,
    sprint_repo: ISprintRepository,
    client_ip: str,
    log_publisher: LogPublisher,
):
    user_id = data.user_id
    email = data.email
    category = data.category
    duration = data.duration
    started_at = data.started_at

    error_message = None

    try:
        category_id = await sprint_repo.get_category_id_by_name(user_id, category)

        await sprint_repo.save_sprint_to_db(
            user_id=user_id,
            category_id=category_id,
            duration=duration,
            started_at=started_at,
        )
        success = True
    except Exception as e:
        error_message = str(e)
        success = False
        print(e)
    finally:
        asyncio.create_task(
            log_save_sprint_attempt(
                log_publisher=log_publisher,
                user_id=user_id,
                email=email,
                success=success,
                duration=duration,
                ip=client_ip,
                error=error_message,
            )
        )
