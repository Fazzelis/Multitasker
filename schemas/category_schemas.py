from pydantic import BaseModel
from uuid import UUID


class CategoryDto(BaseModel):
    name: str


class CategoryDtoPatch(BaseModel):
    new_name: str
    id: UUID


class CategoryDtoDelete(BaseModel):
    id: UUID
