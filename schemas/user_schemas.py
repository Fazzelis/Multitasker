from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr


class NewUserName(BaseModel):
    new_user_name: str


class UserCreateAndAuthorization(UserBase):
    password: str


class UserProfileWithoutPassword(UserBase):
    name: str | None
    avatar_id: UUID | None


class UserNewPassword(UserBase):
    verify_code: str
    new_password: str


class UserSetAvatar(BaseModel):
    avatar_id: UUID
