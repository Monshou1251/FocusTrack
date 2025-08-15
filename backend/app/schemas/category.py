from datetime import datetime

from pydantic import BaseModel


class PCategoryModel(BaseModel):
    user_id: int
    name: str
    created_at: datetime


class CreateCategoryRequest(BaseModel):
    name: str


class UpdateCategoryRequest(BaseModel):
    name: str


class CreateCategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime


class UpdateCategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
