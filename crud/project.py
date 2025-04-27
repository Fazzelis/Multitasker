from fastapi import Depends, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta

from models import *
from schemas.user_schemas import *
from schemas.token_schemas import *
from schemas.category_schemas import *
from schemas.project_schemas import *
from schemas.task_schemas import *
from schemas.sub_task_schemas import *
from utils import *
from sqlalchemy import exists


def post_project(db: Session, project_name: str, user_id: UUID, category_id: UUID):
    project_is_exist = db.query(exists().where(
        Project.name == project_name,
        Project.user_id == user_id
    )).scalar()

    if project_is_exist:
        raise HTTPException(status_code=409, detail="Проект уже существует")

    category_is_exist = db.query(exists().where(
        Category.id == category_id
    )).scalar()

    if not category_is_exist:
        raise HTTPException(status_code=409, detail="Категория, к которой создается проект не найдена")

    new_project = Project(
        name=project_name,
        user_id=user_id,
        category_id=category_id
    )
    db.add(new_project)
    db.commit()
    return ProjectDtoWithCategoryId(
        name=new_project.name,
        category_id=new_project.category_id
    )


def patch_project(db: Session, old_project_name: str, new_project_name: str, user_id: UUID) -> ProjectDto:
    project = db.query(Project).filter(Project.user_id == user_id).filter(Project.name.like(old_project_name)).one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = new_project_name
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectDto(
        name=new_project_name
    )


def delete_project(db: Session, user_id: UUID, project_name: str) -> ProjectDto:
    project = db.query(Project).filter(Project.user_id == user_id).filter(Project.name.like(project_name)).one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return ProjectDto(
        name=project_name
    )
