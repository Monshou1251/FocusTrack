from dataclasses import dataclass
from datetime import datetime


@dataclass
class CategoryDTO:
    user_id: int
    name: str
    created_at: datetime
