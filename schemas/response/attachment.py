from pydantic import BaseModel

from schemas.attachment_schemas import AttachmentInfo


class AttachmentResponse(BaseModel):
    status: str
    attachment_info: AttachmentInfo
