from pydantic import BaseModel
from typing import Any


class SuccessResponse(BaseModel):
    success: bool = True
    message: str | None
    data: Any | None
    

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    
    