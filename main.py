from fastapi import FastAPI, Depends, HTTPException, UploadFile
import os
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base
from schemas import *
from crud import *
from utils import *
from datetime import datetime


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
    if len(user.password) < 8 or len(user.password) > 16:
        return HTTPException(status_code=422, detail="Password does not pass validation")
    db_user = get_user_by_email(db, user.email)
    if db_user is not None:
        return HTTPException(status_code=409, detail="Email already registered")
    user.password = get_password_hash(user.password)

    created_user = post_user(db, user)
    return {"status": "success", "id": str(created_user.id)}


@app.post("/authorization")
def authorization(user: UserAuthorization, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not found")
    if match_hash(user.password, db_user.hashed_password):
        return UserProfile(
            email=db_user.email,
            name=db_user.name,
            avatar=db_user.avatar
        )
    else:
        return HTTPException(status_code=401, detail="Password is not correct")



@app.post("/reset-password")
def request_for_reset_password(payload: UserBase, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, payload.email)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not found")
    hashed_reset_code = generate_and_send_verify_code(payload.email)
    post_reset_code(db, hashed_reset_code, db_user)
    return {"status": "success"}

# в код вшить id пользователя
@app.post("/confirm-reset-password")
def confirm_the_reset(payload: UserNewPassword, db: Session = Depends(get_db)):
    found_code = get_reset_code(db, payload.email)
    if found_code is None:
        return HTTPException(status_code=400, detail="Reset code for this user not found")
    if match_hash(payload.verify_code, found_code.hashed_code):
        if datetime.now().time() > found_code.expiration_time:
            return HTTPException(status_code=400, detail="The verify code has expired")
        patch_user_password(db, found_code.user, get_password_hash(payload.new_password))
        delete_reset_code(db, found_code)
        return {"status", "success"}
    else:
        return HTTPException(status_code=400, detail="Reset code is not correct")
