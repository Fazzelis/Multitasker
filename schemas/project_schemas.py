from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr

from schemas.user_schemas import UserProfileWithoutPassword


class ProjectDto(BaseModel):
    project_id: UUID
    name: str


class ProjectDtoCreate(BaseModel):
    name: str


class ProjectDtoPatch(BaseModel):
    project_id: UUID
    new_name: str


class ProjectDtoDelete(BaseModel):
    id: UUID


class ProjectDtoInfo(ProjectDto):
    creator_id: UUID
    category_name: str | None
    members: List[UserProfileWithoutPassword]


class ProjectDtoWithMemberId(BaseModel):
    project_id: UUID
    member_id: UUID


class ProjectDtoWithMemberEmail(BaseModel):
    project_id: UUID
    member_email: EmailStr


class ProjectDtoWithCategoryId(BaseModel):
    project_id: UUID
    category_id: UUID


class ProjectDtoWithId(BaseModel):
    project_id: UUID
