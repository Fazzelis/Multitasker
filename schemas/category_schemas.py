from pydantic import BaseModel
from uuid import UUID


class CategoryDto(BaseModel):
    name: str


class CategoryDtoPatchDelete(BaseModel):
    new_name: str
    id: UUID
