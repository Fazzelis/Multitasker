from uuid import UUID
from sqlalchemy.orm import Session
from models import Avatar


def get_avatar_by_user_id(db: Session, user_id: UUID) -> Avatar | None:
    return db.query(Avatar).filter(Avatar.user_id == user_id).one_or_none()


def get_avatar_id_by_user_id(db: Session, user_id: UUID) -> UUID | None:
    db_avatar = db.query(Avatar).filter(Avatar.user_id == user_id).one_or_none()
    if db_avatar is None:
        return None
    return db_avatar.id
