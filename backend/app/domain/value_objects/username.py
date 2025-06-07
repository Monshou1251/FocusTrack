from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject


@dataclass(frozen=True, repr=False)
class Username(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()
        if not (3 <= len(self.value) <= 30):
            raise ValueError("Username length must be between 3 and 30 characters")
