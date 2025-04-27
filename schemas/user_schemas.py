from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr


class NewUserName(BaseModel):
    new_user_name: str


class UserCreate(UserBase):
    password: str


class UserAuthorization(UserBase):
    password: str


class UserProfileWithoutPassword(UserBase):
    name: str | None
    avatar_id: UUID


class UserNewPassword(UserBase):
    verify_code: str
    new_password: str
