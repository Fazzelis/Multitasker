from fastapi import Depends, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta

from models import *
from schemas import *
from utils import *


def get_user_by_id(db: Session, id: uuid) -> User | None:
    return db.query(User).filter(User.id.like(id)).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email.like(email)).first()


def post_user(db: Session, new_user: UserCreate) -> User | None:
    db_user = User(
        email=new_user.email,
        name=new_user.email,
        hashed_password=new_user.password
    )
    db.add(db_user)
    db.commit()
    return db_user


def patch_user_password(db: Session, user: User, new_password_hash: str) -> None:
    user.hashed_password = new_password_hash
    db.add(user)
    db.commit()


def post_reset_code(db: Session, hashed_code: str, db_user: User) -> ResetCode | None:
    db_code = ResetCode(hashed_code=hashed_code, expiration_time=((datetime.now() + timedelta(minutes=30)).time()), user_id=db_user.id)
    db.add(db_code)
    db.commit()
    return db_code


def get_reset_code(db: Session, email: str) -> ResetCode | None:
    found_user = db.query(User).filter(User.email.like(email)).first()
    if found_user is not None:
        return found_user.reset_code
    else:
        return None


def delete_reset_code(db: Session, code: ResetCode) -> None:
    db.delete(code)
    db.commit()


def patch_user_name(db: Session, new_name: str, email: str) -> UserProfileWithoutPassword:
    db_user = db.query(User).filter(User.email.like(email)).first()
    db_user.name = new_name
    db.add(db_user)
    db.commit()
    return UserProfileWithoutPassword(
        email=db_user.email,
        name=db_user.name,
        avatar_path=db_user.avatar
    )


def patch_user_avatar(db: Session, email: str, avatar) -> UserProfileWithoutPassword:
    avatar_path = save_user_avatar(email, avatar)
    db_user = db.query(User).filter(User.email.like(email)).first()
    db_user.avatar = avatar_path
    db.add(db_user)
    db.commit()
    return UserProfileWithoutPassword(
        email=db_user.email,
        name=db_user.name,
        avatar_path=db_user.avatar
    )


def get_user_via_jwt(db: Session, email: str):
    db_user = get_user_by_email(db=db, email=email)
    if db_user is not None:
        return UserProfileWithoutPassword(
            email=db_user.email,
            name=db_user.name,
            avatar_path=db_user.avatar
        )
    else:
        raise HTTPException(
            status_code=401,
            detail="token invalid"
        )


def path_user_email(db: Session, email: str, new_email: str):
    db_user = db.query(User).filter(User.email.like(email)).first()
    db_user.email = new_email
    db.add(db_user)
    db.commit()
    new_payload = {
        "sub": str(db_user.id),
        "email": db_user.email
    }
    new_token = encode_jwt(payload=new_payload)
    token_info = TokenInfo(
        token=new_token,
        token_type="Bearer"
    )
    user_password_without_password = UserProfileWithoutPassword(
        email=db_user.email,
        name=db_user.name,
        avatar_path=db_user.avatar
    )
    return {
        "UserInfo": user_password_without_password,
        "TokenInfo": token_info
    }


def post_category(db: Session, user_id: UUID, category_name: str):
    new_category = Category(
        name=category_name,
        user_id=user_id
    )
    db.add(new_category)
    db.commit()
    return {
        "CategoryName": new_category.name,
        "UserId": new_category.user_id,
        "UserName": new_category.user.name
    }


def patch_category(db: Session, user_id: UUID, old_category_name: str, new_category_name: str):
    old_category = db.query(Category).filter(Category.user_id == user_id).filter(Category.name.like(old_category_name)).first()
    if not old_category:
        raise HTTPException(status_code=404, detail="Category not found")
    old_category.name = new_category_name
    db.add(old_category)
    db.commit()
    return {
        "id": old_category.id,
        "NewName": new_category_name
    }


def delete_category(db: Session, user_id: UUID, category_name: str):
    category = db.query(Category).filter(Category.user_id == user_id).filter(Category.name.like(category_name)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {
        "DeletedCategoryId": category.id,
        "DeletedCategoryName": category.name
    }


def post_project(db: Session, project_name: str, user_id: UUID, category_id: UUID):
    new_project = Project(
        name=project_name,
        user_id=user_id,
        category_id=category_id
    )
    db.add(new_project)
    db.commit()
    return {
        "name": new_project.name,
        "category_id": new_project.category_id,
        "user_id": user_id
    }


def set_project_avatar(db: Session, project_name: str, user_id: UUID, user_email: str, avatar: UploadFile) -> str:
    project = db.query(Project).filter(Project.user_id == user_id).filter(Project.name.like(project_name)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    avatar_path = save_project_avatar(user_email, project_name, avatar)
    project.avatar_path = avatar_path
    db.add(project)
    db.commit()
    return "Avatar saved"


def patch_project(db: Session, old_project_name: str, new_project_name: str, user_id: UUID) -> str:
    project = db.query(Project).filter(Project.user_id == user_id).filter(Project.name.like(old_project_name)).one_or_none() # get or none
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = new_project_name
    db.add(project)
    db.commit()
    db.refresh(project) # добавить refresh
    return "Project edited"


def delete_project(db: Session, user_id: UUID, project_name: str) -> str:
    project = db.query(Project).filter(Project.user_id == user_id).filter(Project.name.like(project_name)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return "Project deleted"
