from pydantic import BaseModel

from schemas.user_schemas import UserProfileWithoutPassword


class UserResponse(BaseModel):
    status: str
    info_about_user: UserProfileWithoutPassword
