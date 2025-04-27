from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Project, Task
from schemas.task_schemas import *


def post_task(db: Session, payload: TaskCreate, user_id: UUID):
    db_project = db.query(Project).filter(Project.id == payload.project_id).one_or_none()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Проект не найден")
    task = db.query(Task).filter(Task.name.like(payload.name)).one_or_none()
    if task is not None:
        raise HTTPException(status_code=409, detail="Задача с таким названием уже существует")
    new_task = Task(
        name=payload.name,
        description=payload.description,
        due_date=payload.due_date,
        indicator=payload.indicator,
        user_id=user_id,
        project_id=payload.project_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskBase(
        name=new_task.name,
        description=new_task.description,
        due_date=new_task.due_date,
        indicator=new_task.indicator,
        executor=user_id
    )


def get_all_tasks(db: Session, user_id: UUID):
    tasks = db.query(Task).filter(Task.user_id)


def patch_task(db: Session, payload: TaskPatch, user_id: UUID):
    task = db.query(Task).filter(Task.name.like(payload.name)).one_or_none()
    if task is not None:
        raise HTTPException(status_code=409, detail="Задача с таким именем уже существует")
    task = db.query(Task).filter(Task.id == payload.task_id).one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Задача для изменения не найдена")
    task.name = payload.name
    task.description = payload.description
    task.due_date = payload.due_date
    task.indicator = payload.indicator
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskBase(
        name=task.name,
        description=task.description,
        due_date=task.due_date,
        indicator=task.indicator,
        executor=user_id
    )


def delete_task(db: Session, task_id: UUID, user_id: UUID):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    db.delete(task)
    db.commit()
    return TaskBase(
        name=task.name,
        description=task.description,
        due_date=task.due_date,
        indicator=task.indicator,
        executor=user_id
    )
