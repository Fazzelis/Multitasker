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
            payload: ProjectDtoCreate,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            return ProjectResponse(
                status="success",
                project=post_project(self.db, payload.name, uuid.UUID(decoded_token["sub"]))
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
            return ProjectResponse(
                status="success",
                project=patch_project(self.db, new_project.project_id, new_project.new_name, uuid.UUID(payload.get("sub")))
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def get_all_projects(
            self,
            credentials: HTTPAuthorizationCredentials
    ) -> AllProjectsResponse:
        try:
            token = credentials.credentials
            payload = decode_jwt(token)
            user_id = uuid.UUID(payload.get("sub"))
            return AllProjectsResponse(
                status="success",
                projects=get_all_projects(self.db, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def add_member_into_project(
            self,
            payload: ProjectDtoWithMemberId,
            credentials: HTTPAuthorizationCredentials
    ) -> ProjectResponse:
        try:
            token = credentials.credentials
            decoded_jwt = decode_jwt(token)
            user_id = uuid.UUID(decoded_jwt.get("sub"))
            return ProjectResponse(
                status="success",
                project=add_member_into_project(self.db, user_id, payload.new_member_id, payload.project_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def add_category(
            self,
            payload: ProjectDtoWithCategoryId,
            credentials: HTTPAuthorizationCredentials
    ) -> ProjectResponse:
        try:
            token = credentials.credentials
            decoded_jwt = decode_jwt(token)
            user_id = uuid.UUID(decoded_jwt.get("sub"))
            return ProjectResponse(
                status="success",
                project=add_category(self.db, user_id, payload.project_id, payload.category_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def remove_category(
            self,
            payload: ProjectDtoWithId,
            credentials: HTTPAuthorizationCredentials
    ) -> ProjectResponse:
        try:
            token = credentials.credentials
            decoded_jwt = decode_jwt(token)
            user_id = uuid.UUID(decoded_jwt.get("sub"))
            return ProjectResponse(
                status="success",
                project=remove_category(self.db, user_id, payload.project_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def remove_project(
            self,
            project: ProjectDtoDelete,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            return ProjectResponse(
                status="Project was deleted",
                project=delete_project(self.db, uuid.UUID(payload.get("sub")), project.id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
