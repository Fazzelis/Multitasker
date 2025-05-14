from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User, ResetCode, Attachment
from schemas.user_schemas import UserCreateAndAuthorization, UserProfileWithoutPassword


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).one_or_none()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email.like(email)).one_or_none()


def post_user(db: Session, new_user: UserCreateAndAuthorization) -> User | None:
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
    optional_db_code = db.query(ResetCode).filter(ResetCode.user_id == db_user.id).one_or_none()
    if optional_db_code:
        db.delete(optional_db_code)
        db.commit()
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
    db_avatar = db.query(Attachment).filter(Attachment.id == db_user.avatar_id).one_or_none()
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


def patch_user_avatar(db: Session, user_id: UUID, avatar_id: UUID):
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    db_user.avatar_id = avatar_id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserProfileWithoutPassword(
        email=db_user.email,
        name=db_user.name,
        avatar_id=avatar_id
    )


def get_user_via_jwt(db: Session, user_id: UUID):
    db_user = get_user_by_id(db, user_id)
    db_avatar = db.query(Attachment).filter(Attachment.id == db_user.avatar_id).one_or_none()
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
    db_avatar = db.query(Attachment).filter(Attachment.id == db_user.avatar_id).one_or_none()
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
