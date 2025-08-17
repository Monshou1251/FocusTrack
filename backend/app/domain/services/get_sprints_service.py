from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.interfaces.sprint_repository import ISprintRepository
from app.domain.services.logging_service import (
    log_category_operation_attempt,
)


async def get_sprints_service(
    sprint_repo: ISprintRepository,
    user_id: int,
    email: str,
    client_ip: str,
    log_publisher: LogPublisher,
):
    try:
        sprints = await sprint_repo.get_sprints_from_db(user_id)

        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="get_sprints",
            user_id=user_id,
            email=email,
            category_id=None,
            category_name=None,
            ip=client_ip,
            success=True,
            extra={"sprints_count": len(sprints)},
        )

        return {"sprints": sprints}

    except Exception as e:
        await log_category_operation_attempt(
            log_publisher=log_publisher,
            event="get_sprints",
            user_id=user_id,
            email=email,
            category_id=None,
            category_name=None,
            ip=client_ip,
            success=False,
            error=str(e),
        )
        raise
