from fastapi import HTTPException
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials

from service_utils.sub_task import post_sub_task, get_sub_task, patch_sub_task, delete_sub_task, get_my_sub_tasks
from schemas.response.sub_task import SubTaskResponse, SubTaskDeleteResponse, SubTaskCreateResponse, MySubTasks
from schemas.sub_task_schemas import SubTaskInfo, SubTaskPatch, SubTaskGetDelete, SubTaskSchemas
from utils import decode_jwt
import uuid


class SubTaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_sub_task(
            self,
            payload: SubTaskSchemas,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            user_id = uuid.UUID(decoded_token["sub"])
            return SubTaskCreateResponse(
                status="success",
                sub_task=post_sub_task(db=self.db, payload=payload, user_id=user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def sub_task_info(
            self,
            payload: SubTaskGetDelete,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            user_id = uuid.UUID(decoded_token["sub"])
            return SubTaskResponse(
                status="success",
                sub_task=get_sub_task(db=self.db, sub_task_id=payload.id, user_id=user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def get_my_sub_tasks(
            self,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            user_id = uuid.UUID(decoded_token["sub"])
            return MySubTasks(
                status="success",
                sub_tasks=get_my_sub_tasks(self.db, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def patch_sub_task(
            self,
            payload: SubTaskPatch,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            user_id = uuid.UUID(decoded_token["sub"])
            return SubTaskResponse(
                status="success",
                sub_task=patch_sub_task(db=self.db, payload=payload, user_id=user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def delete_sub_task(
            self,
            payload: SubTaskGetDelete,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            user_id = uuid.UUID(decoded_token["sub"])
            delete_sub_task(self.db, payload.id, user_id)
            return SubTaskDeleteResponse(
                status="success",
                detail="Sub task deleted"
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
