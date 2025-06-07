import re
from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject


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
        # Пример: username должен быть от 3 до 30 символов, только буквы, цифры, подчёркивания
        if not (3 <= len(self.value) <= 30):
            raise ValueError("Username length must be between 3 and 30 characters")
        if not re.match(r"^\w+$", self.value):
            raise ValueError(
                "Username can contain only letters, digits, and underscores"
            )
