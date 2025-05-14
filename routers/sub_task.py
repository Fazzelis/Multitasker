from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database.get_database import get_db
from schemas.response.sub_task import SubTaskResponse, SubTaskDeleteResponse, SubTaskCreateResponse, MySubTasks
from schemas.sub_task_schemas import SubTaskInfo, SubTaskPatch, SubTaskGetDelete, SubTaskSchemas
from service.sub_task_service import SubTaskService

router = APIRouter(
    prefix="/sub-task",
    tags=["Sub-Task"]
)

http_bearer = HTTPBearer()


@router.post("/create-sub-task", response_model=SubTaskCreateResponse)
def create_sub_task(
        payload: SubTaskSchemas,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return SubTaskService(db).create_sub_task(payload=payload, credentials=credentials)


@router.post("/sub-task-info", response_model=SubTaskResponse)
def sub_task_info(
        payload: SubTaskGetDelete,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return SubTaskService(db).sub_task_info(payload, credentials)


@router.get("/get-my-sub-tasks", response_model=MySubTasks)
def get_my_sub_tasks(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return SubTaskService(db).get_my_sub_tasks(credentials)


@router.patch("/patch-sub-task", response_model=SubTaskResponse)
def patch_sub_task(
        payload: SubTaskPatch,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return SubTaskService(db).patch_sub_task(payload, credentials)


@router.delete("/delete-sub-task", response_model=SubTaskDeleteResponse)
def delete_sub_task(
        payload: SubTaskGetDelete,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return SubTaskService(db).delete_sub_task(payload, credentials)
