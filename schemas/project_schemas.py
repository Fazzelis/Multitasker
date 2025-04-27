from pydantic import BaseModel
from uuid import UUID


class ProjectDto(BaseModel):
    name: str


class ProjectDtoWithCategoryId(ProjectDto):
    category_id: UUID


class ProjectDtoPatch(ProjectDto):
    new_name: str
