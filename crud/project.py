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


def post_project(db: Session, project_name: str, user_id: UUID):
    new_project = Project(
        name=project_name,
        creator_id=user_id,
    )
    db.add(new_project)
    db.flush()

    user = db.query(User).filter(User.id == user_id).first()
    user.projects.append(new_project)

    db.commit()
    db.refresh(new_project)
    return ProjectDto(
        project_id=new_project.id,
        name=new_project.name
    )


def patch_project(db: Session, project_id: UUID, new_project_name: str, user_id: UUID) -> ProjectDto:
    project = db.query(Project).filter(Project.creator_id == user_id).filter(Project.id == project_id).one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = new_project_name
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectDto(
        project_id=project.id,
        name=new_project_name
    )


def get_all_projects(db: Session, user_id: UUID) -> [ProjectDtoInfo]:
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    db_projects = db_user.projects.all()
    response = []
    for db_project in db_projects:
        temp_users = db_project.users
        temp_users_dto = []
        for user in temp_users:
            temp_users_dto.append(UserProfileWithoutPassword(
                email=user.email,
                name=user.name,
                avatar_id=user.avatar_id
            ))
        response.append(ProjectDtoInfo(
            project_id=db_project.id,
            name=db_project.name,
            creator_id=db_project.creator_id,
            members=temp_users_dto
        ))
    return response


def add_member_into_project(db: Session, user_id: UUID, member_id: UUID, project_id: UUID):
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    db_project = db.query(Project).filter(Project.id == project_id).one_or_none()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if db_project.creator_id != user_id and not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    db_new_member = db.query(User).filter(User.id == member_id).one_or_none()
    if not db_new_member:
        # Написать логику приглашения в приложение с помощью отправки сообщения на почту
        raise HTTPException(status_code=404, detail="User not found")
    if db_new_member not in db_project.users:
        db_project.users.append(db_new_member)
    else:
        raise HTTPException(status_code=409, detail="User already member")
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return ProjectDto(
        project_id=db_project.id,
        name=db_project.name
    )


def add_category(db: Session, user_id: UUID, project_id: UUID, category_id: UUID) -> ProjectDto:
    db_project = db.query(Project).filter(Project.id == project_id).one_or_none()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_category = db.query(Category).filter(Category.id == category_id).one_or_none()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    if db_user not in db_project.users:
        raise HTTPException(status_code=403, detail="Access denied")
    db_category.projects.append(db_project)
    db.add(db_category)
    db.commit()
    db.refresh(db_project)
    return ProjectDto(
        project_id=db_project.id,
        name=db_project.name
    )


def remove_category(db: Session, user_id: UUID, project_id: UUID) -> ProjectDto:
    db_project = db.query(Project).filter(Project.id == project_id).one_or_none()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    if db_user not in db_project.users and not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    db_category = db.query(Category).filter(Category.user_id == user_id).one_or_none()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.projects.remove(db_project)
    return ProjectDto(
        project_id=db_project.id,
        name=db_project.name
    )


def delete_project(db: Session, user_id: UUID, project_id: UUID) -> ProjectDto:
    db_project = db.query(Project).filter(Project.id == project_id).one_or_none()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    if db_project.creator_id != user_id and not db_user.is_admin:
        if db_user in db_project.users:
            db_project.users.remove(db_user)
            db.add(db_project)
            db.commit()
            return ProjectDto(
                project_id=db_project.id,
                name=db_project.name
            )
    db.delete(db_project)
    db.commit()
    return ProjectDto(
        project_id=db_project.id,
        name=db_project.name
    )
