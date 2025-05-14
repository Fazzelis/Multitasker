import mimetypes
from uuid import UUID

from fastapi import UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from schemas.attachment_schemas import AttachmentDelete
from schemas.response.attachment import AttachmentResponse
from service_utils.attachment import post_file, get_attachment_info, delete_attachment


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

    def get_file(self, file_id: UUID):
        db_file = get_attachment_info(self.db, file_id)
        if not os.path.exists(db_file.path):
            raise HTTPException(status_code=404, detail="File not found in directory")
        filename = os.path.basename(db_file.path)
        mime_type, _ = mimetypes.guess_type(db_file.path)
        if mime_type is None:
            mime_type = "application/octet-stream"
        return FileResponse(
            path=db_file.path,
            filename=filename,
            media_type=mime_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
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
