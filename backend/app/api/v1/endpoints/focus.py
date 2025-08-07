from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.core.dependencies import (
    get_log_publisher,
    get_sprint_repository,
)
from app.core.security.user_security import get_current_user
from app.domain.dto.sprint_dto import SprintSaveDTO
from app.domain.interfaces.log_publisher import LogPublisher
from app.domain.interfaces.sprint_repository import (
    ISprintRepository,
)
from app.domain.services.save_sprint_service import save_sprint_service
from app.schemas.sprint import PSprintSaveModel

router = APIRouter()


@router.post("/save_sprint")
async def save_sprint(
    request: Request,
    data: PSprintSaveModel,
    current_user=Depends(get_current_user),
    sprint_repo: ISprintRepository = Depends(get_sprint_repository),
    log_publisher: LogPublisher = Depends(get_log_publisher),
):
    client_ip = request.client.host if request.client else "unknown"

    dto = SprintSaveDTO(
        user_id=current_user.id.value,
        email=current_user.email.value,
        category=data.category,
        duration=data.duration,
        started_at=data.started_at,
    )
    print("current_user:", current_user)
    print("client_ip: ", client_ip)
    print("data")
    print(data)

    await save_sprint_service(dto, sprint_repo, client_ip, log_publisher)

    return JSONResponse(content={"message": "Sprint received"}, status_code=200)
