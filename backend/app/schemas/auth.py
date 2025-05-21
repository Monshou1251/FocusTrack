from pydantic import BaseModel, EmailStr
from fastapi import Form

class UserAuthForm(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        password: str = Form(...)
    ) -> "UserAuthForm":
        return cls(email=email, password=password)
