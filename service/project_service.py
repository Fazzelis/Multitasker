import uuid

from fastapi import File
from fastapi.security import HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session

from crud.project import *
from schemas.project_schemas import *
from utils import *
from schemas.response.project import *


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(
            self,
            payload: ProjectDtoWithCategoryId,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            return ProjectResponse(
                status="success",
                project=post_project(self.db, payload.name, uuid.UUID(decoded_token["sub"]), payload.category_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def edit_project(
            self,
            new_project: ProjectDtoPatch,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token)
            return ProjectResponseWithoutCategoryId(
                status="success",
                project=patch_project(self.db, new_project.name, new_project.new_name, uuid.UUID(payload.get("sub")))
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def remove_project(
            self,
            project: ProjectDto,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            return ProjectResponseWithoutCategoryId(
                status="Project was deleted",
                project=delete_project(self.db, uuid.UUID(payload.get("sub")), project.name)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
