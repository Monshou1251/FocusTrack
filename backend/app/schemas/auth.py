from fastapi import Form


class UserAuthForm:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
