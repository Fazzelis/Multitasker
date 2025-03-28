from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: str
    password: str


class UserAuthorization(UserBase):
    password: str


class UserProfile(UserCreate):
    avatar_path: str


class UserNewPassword(UserBase):
    verify_code: str
    new_password: str
