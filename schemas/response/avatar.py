from pydantic import BaseModel
from schemas.avatar_schemas import AvatarBase


class AvatarResponse(BaseModel):
    status: str
    avatar_info: AvatarBase
