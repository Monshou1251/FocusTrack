from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm

class UserAuthForm(BaseModel):
    email: EmailStr = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

    @classmethod
    def as_form(cls, email: str = Form(...), password: str = Form(...)):
        return cls(email=email, password=password)


class EmailLoginForm(UserAuthForm):
    password: str = Field(..., min_length=6)


class EmailRegisterForm(UserAuthForm): ...
