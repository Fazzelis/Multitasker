from pydantic import BaseModel
from uuid import UUID


class CategoryDto(BaseModel):
    category_id: UUID
    name: str


class CategoryDtoCreate(BaseModel):
    name: str


class CategoryDtoPatch(BaseModel):
    category_id: UUID
    new_name: str


class CategoryDtoDelete(BaseModel):
    category_id: UUID
