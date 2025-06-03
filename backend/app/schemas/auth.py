from pydantic import BaseModel, EmailStr, Field


class UserAuthForm(BaseModel):
    email: EmailStr = Field(..., min_length=1)
    password: str = Field(..., min_length=6)

class EmailLoginForm(UserAuthForm): ...

class EmailRegisterForm(UserAuthForm): ...