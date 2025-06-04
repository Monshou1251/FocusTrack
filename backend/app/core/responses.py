from fastapi.responses import JSONResponse


def success_response(message: str, data: dict | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={"success": True, "message": message, "data": data or {}},
    )


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content={"success": False, "message": message}
    )
