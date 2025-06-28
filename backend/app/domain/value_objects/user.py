import re
from dataclasses import dataclass
from urllib.parse import urlparse

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

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, repr=False)
class Username(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()
        if not (3 <= len(self.value) <= 30):
            raise ValueError("Username length must be between 3 and 30 characters")


@dataclass(frozen=True, repr=False)
class AvatarUrl(ValueObject):
    value: str | None

    def __post_init__(self):
        super().__post_init__()
        if self.value is None:
            return
        parsed = urlparse(self.value)
        if not (parsed.scheme and parsed.netloc):
            raise ValueError(f"Invalid URL format: {self.value}")

    def __str__(self):
        return self.value or ""
