from dataclasses import dataclass
from datetime import datetime


@dataclass
class SprintSaveDTO:
    user_id: int
    email: str
    category: str
    duration: int
    started_at: datetime
