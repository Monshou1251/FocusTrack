import re
from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserPasswordHash:
    value: str

    def __str__(self):
        return self.value


@dataclass(frozen=True, repr=False)
class UserId(ValueObject):
    value: int


@dataclass(frozen=True, repr=False)
class Email(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email format: {self.value}")


@dataclass(frozen=True, repr=False)
class Username(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()
        if not (3 <= len(self.value) <= 30):
            raise ValueError("Username length must be between 3 and 30 characters")
