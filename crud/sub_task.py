from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from schemas.sub_task_schemas import SubTaskInfo, SubTaskPatch, SubTaskSchemas
from models import Task, User, SubTask, Project


def post_sub_task(db: Session, payload: SubTaskSchemas, user_id: UUID):
    db_task = db.query(Task).filter(Task.id == payload.task_id).one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    if db_user.id != db_task.creator_id and not db_user.is_admin:
        db_project = db.query(Project).filter(Project.id == db_task.project_id).one_or_none()
        if user_id != db_project.creator_id:
            raise HTTPException(status_code=403, detail="Access denied")

    for sub_task in db_task.sub_tasks:
        if payload.name == sub_task.name:
            raise HTTPException(status_code=400, detail="Sub task with this name already exist")

    db_executor = db.query(User).filter(User.email.like(payload.executor_email)).one_or_none()
    if not db_executor:
        raise HTTPException(status_code=404, detail="Executor not found")

    db_sub_task = SubTask(
        name=payload.name,
        description=payload.description,
        due_date=payload.due_date,
        creator_id=user_id,
        task_id=db_task.id,
        executor_email=payload.executor_email,
        indicator=payload.indicator
    )

    db.add(db_sub_task)
    db.commit()
    db.refresh(db_sub_task)

    return SubTaskSchemas(
        sub_task_id=db_sub_task.id,
        name=db_sub_task.name,
        executor_email=db_sub_task.executor_email,
        description=db_sub_task.description,
        due_date=db_sub_task.due_date,
        task_id=db_sub_task.task_id,
        indicator=db_sub_task.indicator,
        creator_id=db_sub_task.creator_id
    )


def get_sub_task(db: Session, sub_task_id: UUID, user_id: UUID) -> SubTaskInfo:
    db_sub_task = db.query(SubTask).filter(SubTask.id == sub_task_id).one_or_none()
    if not db_sub_task:
        raise HTTPException(status_code=404, detail="Sub task not found")

    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    db_task = db.query(Task).filter(Task.id == db_sub_task.task_id).one_or_none()
    db_project = db.query(Project).filter(Project.id == db_task.project_id).one_or_none()

    if db_user not in db_project.users and not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    return SubTaskInfo(
        sub_task_id=db_sub_task.id,
        name=db_sub_task.name,
        executor_email=db_sub_task.executor_email,
        description=db_sub_task.description,
        due_date=db_sub_task.due_date,
        task_id=db_task.id,
        indicator=db_sub_task.indicator,
        creator_id=db_sub_task.creator_id
    )


def patch_sub_task(db: Session, payload: SubTaskPatch, user_id: UUID):
    db_sub_task = db.query(SubTask).filter(SubTask.id == payload.sub_task_id).one_or_none()
    if not db_sub_task:
        raise HTTPException(status_code=404, detail="Sub task not found")

    db_task = db.query(Task).filter(Task.id == db_sub_task.task_id).one_or_none()
    for sub_task in db_task.sub_tasks:
        if payload.name == sub_task.name:
            raise HTTPException(status_code=400, detail="Sub task with this name already exist")

    db_executor = db.query(User).filter(User.email == payload.executor_email).one_or_none()
    db_project = db.query(Project).filter(Project.id == db_task.project_id).one_or_none()
    if not db_executor or db_executor not in db_project.users:
        raise HTTPException(status_code=404, detail="Executor not found")

    if payload.name is not None:
        db_sub_task.name = payload.name

    if payload.executor_email is not None:
        db_sub_task.executor_email = payload.executor_email

    if payload.description is not None:
        db_sub_task.description = payload.description

    if payload.due_date is not None:
        db_sub_task.due_date = payload.due_date

    if payload.indicator is not None:
        db_sub_task.indicator = payload.indicator

    db.add(db_sub_task)
    db.commit()
    db.refresh(db_sub_task)

    return SubTaskInfo(
        sub_task_id=db_sub_task.id,
        name=db_sub_task.name,
        executor_email=db_sub_task.executor_email,
        description=db_sub_task.description,
        due_date=db_sub_task.due_date,
        task_id=db_task.id,
        indicator=db_sub_task.indicator,
        creator_id=db_sub_task.creator_id
    )


def delete_sub_task(db: Session, sub_task_id: UUID, user_id: UUID):
    db_sub_task = db.query(SubTask).filter(SubTask.id == sub_task_id).one_or_none()

    if not db_sub_task:
        raise HTTPException(status_code=404, detail="Sub task not found")

    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    db_task = db.query(Task).filter(Task.id == db_sub_task.task_id).one_or_none()
    db_project = db.query(Project).filter(Project.id == db_task.project_id).one_or_none()

    if user_id != db_project.creator_id and not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    db.delete(db_sub_task)
    db.commit()
