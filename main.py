from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base
from schemas import (
    UserBase, UserCreate
)
from crud import (
    get_user_by_id,
    get_user_by_email,
    post_user
)
from utils import (
    get_password_hash
)


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register-user")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user is not None:
        return HTTPException(status_code=409, detail="Email already registered")
    created_user = post_user(db, user)
    return {"status": "success", "id": str(created_user.id)}
