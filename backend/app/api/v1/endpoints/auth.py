from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin
from app.schemas.auth import UserAuthForm
from app.services.user_service import register_user, authenticate_user
 

router = APIRouter()


@router.post("/register")
async def register(
        form_data: Annotated[UserAuthForm, Depends()],
        db: AsyncSession = Depends(get_db)
):
    return await register_user(form_data, db)


@router.post("/login")
async def login(
        form_data: Annotated[UserAuthForm, Depends()],
        db: AsyncSession = Depends(get_db)
):
    return await authenticate_user(form_data, db)
