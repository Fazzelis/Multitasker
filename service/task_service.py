from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from schemas.project_schemas import ProjectDtoWithId
from schemas.task_schemas import *
from utils import decode_jwt
import uuid
from crud.task import *
from schemas.response.task import *


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(
            self,
            new_task: TaskCreate,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = uuid.UUID(payload["sub"])
            return TaskResponse(
                status="success",
                task=post_task(self.db, new_task, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def get_my_tasks(
            self,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = uuid.UUID(payload["sub"])
            return MyTasksResponse(
                status="success",
                tasks=get_my_tasks(self.db, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def view_project_tasks(
            self,
            payload: ProjectDtoWithId,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            user_id = uuid.UUID(decoded_token["sub"])
            return ProjectTasksResponse(
                status="success",
                tasks=view_project_tasks(self.db, payload.project_id, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def edit_task(
            self,
            new_task: TaskPatch,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = uuid.UUID(payload["sub"])
            return TaskResponse(
                status="success",
                task=patch_task(self.db, new_task, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def delete_task(
            self,
            task_id_schema: TaskDelete,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = uuid.UUID(payload["sub"])
            return TaskResponse(
                status="task was deleted",
                task=delete_task(self.db, task_id_schema.task_id, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error
