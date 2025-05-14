from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Attachment
from schemas.attachment_schemas import AttachmentInfo
from utils import save_file


def post_file(
        db: Session,
        file
) -> AttachmentInfo:
    db_attachment = Attachment(
        attachment_path=save_file(file)
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return AttachmentInfo(
        path=db_attachment.attachment_path,
        attachment_id=db_attachment.id
    )


def get_attachment_info(
        db: Session,
        attachment_id: UUID
):
    db_attachment = db.query(Attachment).filter(Attachment.id == attachment_id).one_or_none()
    if not db_attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return AttachmentInfo(
        path=db_attachment.attachment_path,
        attachment_id=db_attachment.id
    )


def delete_attachment(
        db: Session,
        attachment_id: UUID
):
    db_attachment = db.query(Attachment).filter(Attachment.id == attachment_id).one_or_none()
    if not db_attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    response = AttachmentInfo(
        path=db_attachment.attachment_path,
        attachment_id=db_attachment.id
    )
    db.delete(db_attachment)
    db.commit()
    return response
