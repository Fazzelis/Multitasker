from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from schemas.project_schemas import ProjectDtoWithId
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


@router.get("/get-my-tasks", response_model=MyTasksResponse)
def get_my_tasks(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).get_my_tasks(credentials)


@router.post("/view-project-tasks", response_model=ProjectTasksResponse)
def view_project_tasks(
        payload: ProjectDtoWithId,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return TaskService(db).view_project_tasks(payload, credentials)


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
