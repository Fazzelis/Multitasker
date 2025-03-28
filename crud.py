from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta

from models import User, ResetCode
from schemas import *


def get_user_by_id(db: Session, id: uuid) -> User | None:
    return db.query(User).filter(User.id.like(id)).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email.like(email)).first()


def post_user(db: Session, new_user: UserCreate) -> User | None:
    db_user = User(
        email=new_user.email,
        name=new_user.name,
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
