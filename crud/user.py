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
from schemas.avatar_schemas import AvatarBase


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).one_or_none()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email.like(email)).one_or_none()


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
    found_user = db.query(User).filter(User.email.like(email)).one_or_none()
    if found_user is not None:
        return found_user.reset_code
    else:
        return None


def delete_reset_code(db: Session, code: ResetCode) -> None:
    db.delete(code)
    db.commit()


def patch_user_name(db: Session, new_name: str, user_id: UUID) -> UserProfileWithoutPassword:
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    db_avatar = db.query(Avatar).filter(Avatar.user_id == user_id).one_or_none()
    if db_avatar is None:
        avatar_id = None
    else:
        avatar_id = db_avatar.id
    db_user.name = new_name
    db.add(db_user)
    db.commit()
    return UserProfileWithoutPassword(
        email=db_user.email,
        name=db_user.name,
        avatar_id=avatar_id
    )


def patch_user_avatar(db: Session, user_id: UUID, avatar) -> AvatarBase:
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    avatar_path = save_user_avatar(db_user.email, avatar)
    found_avatar = db.query(Avatar).filter(Avatar.user_id == user_id).one_or_none()
    if found_avatar is None:
        found_avatar = Avatar(avatar_path=avatar_path, user_id=user_id)
    else:
        found_avatar.avatar_path = avatar_path
    db.add(found_avatar)
    db.commit()
    return AvatarBase(
        user_id=user_id,
        avatar_path=avatar_path
    )


def get_user_via_jwt(db: Session, user_id: UUID):
    db_user = get_user_by_id(db, user_id)
    db_avatar = db.query(Avatar).filter(Avatar.user_id == user_id).one_or_none()
    if db_avatar is None:
        avatar_id = None
    else:
        avatar_id = db_avatar.id
    if db_user is not None:
        return UserProfileWithoutPassword(
            email=db_user.email,
            name=db_user.name,
            avatar_id=avatar_id
        )
    else:
        raise HTTPException(
            status_code=401,
            detail="token invalid"
        )


def path_user_email(db: Session, user_id: UUID, new_email: str):
    db_user = get_user_by_id(db, user_id)
    db_user.email = new_email
    db_avatar = db.query(Avatar).filter(Avatar.user_id == user_id).first()
    if db_avatar is None:
        avatar_id = None
    else:
        avatar_id = db_avatar.id
    db.add(db_user)
    db.commit()
    user_without_password = UserProfileWithoutPassword(
        email=db_user.email,
        name=db_user.name,
        avatar_id=avatar_id
    )
    return user_without_password
