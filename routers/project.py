from fastapi import APIRouter, File
from fastapi.security import HTTPBearer
from jwt import ExpiredSignatureError
from database.get_database import get_db
from crud.project import *
from crud.user import *
from utils import *
from schemas.project_schemas import *
from service.project_service import ProjectService
from schemas.response.project import *


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)

http_bearer = HTTPBearer()


@router.post("/create-project", response_model=ProjectResponse)
def create_project(
        payload: ProjectDtoWithCategoryId,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db=db).create_project(payload=payload, credentials=credentials)


@router.patch("/edit-project", response_model=ProjectResponseWithoutCategoryId)
def edit_project(
    new_project: ProjectDtoPatch,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    return ProjectService(db=db).edit_project(new_project, credentials)


@router.delete("/remove-project", response_model=ProjectResponseWithoutCategoryId)
def remove_project(
        project: ProjectDto,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db=db).remove_project(project, credentials)
