from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import register_user, authenticate_user

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(user.username, user.email, user.password, db)

@router.post("/login")
async def register(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return await authenticate_user(user.email, user.password, db)
