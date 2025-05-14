from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database.get_database import get_db
from schemas.response.attachment import *
from service.attachment_service import AttachmentService
from schemas.attachment_schemas import *

router = APIRouter(
    prefix="/attachment",
    tags=["Attachment"]
)


@router.post("/upload-attachment", response_model=AttachmentResponse)
def upload_attachment(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    return AttachmentService(db).upload_file(file)


@router.get("/get-attachment", response_class=FileResponse)
def get_attachment(
        attachment_id: UUID,
        db: Session = Depends(get_db)
):
    return AttachmentService(db).get_file(attachment_id)


@router.delete("/delete-attachment", response_model=AttachmentResponse)
def delete_attachment(
        payload: AttachmentDelete,
        db: Session = Depends(get_db)
):
    return AttachmentService(db).delete_file(payload)
