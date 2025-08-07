from datetime import datetime

from pydantic import BaseModel, Field


class PSprintSaveModel(BaseModel):
    category: str = Field(..., min_length=1, max_length=20)
    duration: int = Field(..., ge=1)
    started_at: datetime
