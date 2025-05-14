from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Project, Task, User
from schemas.task_schemas import *


def post_task(db: Session, payload: TaskCreate, user_id: UUID):
    db_project = db.query(Project).filter(Project.id == payload.project_id).one_or_none()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Проект не найден")

    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    if user_id != db_project.creator_id and not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    task = db.query(Task).filter(Task.project_id == payload.project_id).filter(Task.name.like(payload.name)).one_or_none()
    if task is not None:
        raise HTTPException(status_code=409, detail="Задача с таким названием уже существует")

    db_executor = db.query(User).filter(User.email.like(payload.executor_email)).one_or_none()
    if not db_executor:
        raise HTTPException(status_code=404, detail="User for execution not found")

    if db_executor not in db_project.users:
        db_project.users.append(db_executor)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)

    new_task = Task(
        name=payload.name,
        description=payload.description,
        due_date=payload.due_date,
        indicator=payload.indicator,
        creator_id=user_id,
        project_id=payload.project_id,
        executor_email=db_executor.email
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskBase(
        name=new_task.name,
        description=new_task.description,
        due_date=new_task.due_date,
        indicator=new_task.indicator,
        creator=new_task.creator_id,
        executor=new_task.executor_email,
        project_id=new_task.project_id
    )


def get_all_tasks(db: Session, user_id: UUID):
    pass


def patch_task(db: Session, payload: TaskPatch, user_id: UUID):
    db_project = db.query(Project).filter(Project.id == payload.project_id).one_or_none()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    task = db.query(Task).filter(Task.project_id == payload.project_id).filter(Task.name.like(payload.name)).one_or_none()
    if task is not None:
        raise HTTPException(status_code=409, detail="Задача с таким именем уже существует")

    task = db.query(Task).filter(Task.id == payload.task_id).one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Задача для изменения не найдена")

    if task.creator_id != user_id:
        db_user = db.query(User).filter(User.id == user_id).one_or_none()
        if not db_user.is_admin:
            raise HTTPException(status_code=403, detail="Access denied")

    if payload.name != "":
        task.name = payload.name
    if payload.description != "":
        task.description = payload.description
    if payload.due_date != "":
        task.due_date = payload.due_date
    if payload.indicator != "":
        task.indicator = payload.indicator
    if payload.executor_email is not None:
        db_executor = db.query(User).filter(User.email.like(payload.executor_email)).one_or_none()
        if not db_executor:
            raise HTTPException(status_code=404, detail="Executor not found")
        if db_executor not in db_project.users:
            db_project.users.append(db_executor)
            db.add(db_project)
            db.commit()
            db.refresh(db_project)
        task.executor_email = payload.executor_email

    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskBase(
        name=task.name,
        description=task.description,
        due_date=task.due_date,
        indicator=task.indicator,
        creator=task.creator_id,
        executor=task.executor_email,
        project_id=task.project_id
    )


def delete_task(db: Session, task_id: UUID, user_id: UUID):
    task = db.query(Task).filter(Task.id == task_id).one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if user_id != task.creator_id and user_id != task.executor_id:
        db_user = db.query(User).filter(User.id == user_id).one_or_none()
        if not db_user.is_admin:
            raise HTTPException(status_code=403, detail="Access denied")
    db.delete(task)
    db.commit()
    return TaskBase(
        name=task.name,
        description=task.description,
        due_date=task.due_date,
        indicator=task.indicator,
        creator=task.creator_id,
        executor=task.executor_email,
        project_id=task.project_id
    )
