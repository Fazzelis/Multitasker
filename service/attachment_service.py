from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from schemas.response.attachment import *
from crud.attachment import *
import os
from pathlib import Path


class AttachmentService:
    def __init__(self, db: Session):
        self.db = db

    def upload_file(
            self,
            file: UploadFile = File(...)
    ):
        return AttachmentResponse(
            status="success",
            attachment_info=post_file(self.db, file)
        )

    def delete_file(self, payload: AttachmentDelete):
        try:
            attachment_info = get_attachment_info(self.db, payload.attachment_id)
            abs_file = Path(attachment_info.path).absolute()
            if abs_file.exists():
                os.remove(abs_file)
            else:
                raise HTTPException(status_code=404, detail="File not found in directory")
            return AttachmentResponse(
                status="success",
                attachment_info=delete_attachment(self.db, payload.attachment_id)
            )
        except HTTPException as error:
            raise error
