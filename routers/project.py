from fastapi import APIRouter, File, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session

from database.get_database import get_db
from schemas.project_schemas import ProjectDtoCreate, ProjectDtoPatch, ProjectDtoWithMemberEmail, \
    ProjectDtoWithMemberId, ProjectDtoWithCategoryId, ProjectDtoWithId, ProjectDtoDelete
from schemas.response.project import ProjectResponse, AllProjectsResponse, ProjectRemoveMemberResponse
from service.project_service import ProjectService


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)

http_bearer = HTTPBearer()


@router.post("/create-project", response_model=ProjectResponse)
def create_project(
        payload: ProjectDtoCreate,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db=db).create_project(payload=payload, credentials=credentials)


@router.patch("/edit-project", response_model=ProjectResponse)
def edit_project(
    new_project: ProjectDtoPatch,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    return ProjectService(db=db).edit_project(new_project, credentials)


@router.get("/get-projects", response_model=AllProjectsResponse)
def get_all_projects(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db=db).get_projects(credentials)


@router.patch("/add-member-into-project", response_model=ProjectResponse)
def add_member_into_project(
        payload: ProjectDtoWithMemberEmail,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db).add_member_into_project(payload, credentials)


@router.delete("/remove-member-from-project", response_model=ProjectRemoveMemberResponse)
def remove_member_from_project(
        payload: ProjectDtoWithMemberId,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db).remove_member_from_project(payload, credentials)


@router.patch("/add-category", response_model=ProjectResponse)
def add_category(
        payload: ProjectDtoWithCategoryId,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db).add_category(payload, credentials)


@router.patch("/remove-category", response_model=ProjectResponse)
def remove_category(
        payload: ProjectDtoWithId,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db).remove_category(payload, credentials)


@router.delete("/remove-project", response_model=ProjectResponse)
def remove_project(
        project: ProjectDtoDelete,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return ProjectService(db=db).remove_project(project, credentials)
