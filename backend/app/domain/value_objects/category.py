from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject


@dataclass(frozen=True, repr=False)
class CategoryId(ValueObject):
    value: int


@dataclass(frozen=True, repr=False)
class CategoryName(ValueObject):
    value: str

    def __post_init__(self):
        super().__post_init__()
        cleaned = self.value.strip()
        if not (3 <= len(cleaned) <= 18):
            raise ValueError("Category length must be between 3 and 18 characters")
        object.__setattr__(self, "value", cleaned)
