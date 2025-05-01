from pydantic import BaseModel
from uuid import UUID


class AttachmentBase(BaseModel):
    path: str


class AttachmentInfo(AttachmentBase):
    attachment_id: UUID


class AttachmentDelete(BaseModel):
    attachment_id: UUID
