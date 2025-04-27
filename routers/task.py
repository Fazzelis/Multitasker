from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas.task_schemas import *
from sqlalchemy.orm import Session
from database.get_database import get_db
from service.task_service import TaskService
from schemas.response.task import *


router = APIRouter(
    prefix="/task",
    tags=["Task"]
)

http_bearer = HTTPBearer()


@router.post("/create-task", response_model=TaskResponse)
def create_task(
    payload: TaskCreate,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    return TaskService(db).create_task(new_task=payload, credentials=credentials)


@router.get("/get-all-tasks")
def get_all_tasks(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).get_all_tasks(credentials)


@router.patch("/edit-task", response_model=TaskResponse)
def edit_task(
        new_task: TaskPatch,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).edit_task(new_task, credentials)


@router.delete("/delete-task", response_model=TaskResponse)
def delete_task(
        task_id_schema: TaskDelete,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).delete_task(task_id_schema, credentials)
