from fastapi.responses import JSONResponse
from app.schemas.responses_schemas import SuccessResponse, ErrorResponse
from typing import Any


def success_response(message: str = "", data: Any = None) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=SuccessResponse(message=message, data=data).model_dump()
    )
    
def error_response(error: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(error=error).model_dump()
    )