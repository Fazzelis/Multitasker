from pydantic import BaseModel
from uuid import UUID


class AvatarBase(BaseModel):
    user_id: UUID
    avatar_path: str
