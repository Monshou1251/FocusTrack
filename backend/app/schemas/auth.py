from pydantic import BaseModel, EmailStr
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm

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


class OAuth2EmailRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        email: str = Form(..., alias="username"),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: str = Form(None),
        client_secret: str = Form(None),
    ):
        super().__init__(
            username=email,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret
        )

    @property
    def email(self) -> str:
        return self.username  # alias