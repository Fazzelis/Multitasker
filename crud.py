from sqlalchemy.orm import Session
import uuid

from models import User
from schemas import UserBase, UserCreate
# from utils import


def get_user_by_id(db: Session, id: uuid):
    return db.query(User).filter(User.id.like(id)).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email.like(email)).first()


def post_user(db: Session, new_user: UserCreate):
    db_user = User(email=new_user.email, hashed_password=new_user.password)
    db.add(db_user)
    db.commit()
    return db_user
