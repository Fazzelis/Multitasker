from typing import List
from uuid import UUID

from pydantic import BaseModel

from schemas.user_schemas import UserProfileWithoutPassword


class ProjectDto(BaseModel):
    name: str


class ProjectDtoPatch(ProjectDto):
    new_name: str


class ProjectDtoDelete(BaseModel):
    id: UUID


class ProjectDtoInfo(ProjectDto):
    creator_id: UUID
    members: List[UserProfileWithoutPassword]


class ProjectDtoWithMemberId(BaseModel):
    id: UUID
    new_member_id: UUID


class ProjectDtoWithCategoryId(BaseModel):
    project_id: UUID
    category_id: UUID


class ProjectDtoWithId(BaseModel):
    project_id: UUID
