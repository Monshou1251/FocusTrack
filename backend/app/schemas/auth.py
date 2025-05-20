from fastapi import Form
from pydantic import BaseModel, EmailStr

class UserAuthForm:
    def __init__(self, email: EmailStr, password: str):
        self.email = email
        self.password = password
