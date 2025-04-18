import uuid

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class NewUserName(BaseModel):
    new_user_name: str


class NewUserEmail(BaseModel):
    new_user_email: str


class UserCreate(UserBase):
    password: str


class UserAuthorization(UserBase):
    password: str


class UserProfileWithoutPassword(UserBase):
    name: str | None
    avatar_path: str | None


class UserNewPassword(UserBase):
    verify_code: str
    new_password: str


class TokenInfo(BaseModel):
    token: str
    token_type: str


class CategoryDto(BaseModel):
    name: str


class CategoryDtoPatch(CategoryDto):
    new_name: str


class ProjectDto(BaseModel):
    name: str


class ProjectDtoWithCategoryId(ProjectDto):
    category_id: str


class ProjectDtoPatch(ProjectDto):
    new_name: str


class Task(BaseModel):
    name: str
    description: str
    due_date: str
    indicator: int

