# schemas/user.py
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str | None = None
    avatar_url: str | None = None
