from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/save_sprint")
async def save_sprint(request: Request):
    body = await request.json()
    print("💾 Received focus session:", body)  # Заглушка: просто печатаем

    return JSONResponse(content={"message": "Sprint received"}, status_code=200)
