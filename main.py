from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base
from schemas import *
from crud import *
from utils import *
from datetime import datetime


app = FastAPI()
http_bearer = HTTPBearer()

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

    jwt_payload = {
        "sub": str(created_user.id),
        "email": created_user.email
    }
    token = encode_jwt(payload=jwt_payload)
    token_info = TokenInfo(
        token=token,
        token_type="Bearer"
    )
    return {"status": "success", "token_info": token_info}


@app.post("/authorization")
def authorization(user: UserAuthorization, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not found")
    if match_hash(user.password, db_user.hashed_password):
        jwt_payload = {
            "sub": str(db_user.id),
            "email": db_user.email
        }
        token = encode_jwt(payload=jwt_payload)
        token_info = TokenInfo(
            token=token,
            token_type="Bearer"
        )
        user_info = UserProfileWithoutPassword(
            email=db_user.email,
            name=db_user.name,
            avatar_path=db_user.avatar
        )
        return {
            "status": "success",
            "UserInfo": user_info,
            "TokenInfo": token_info
        }
    else:
        return HTTPException(status_code=401, detail="Password is not correct")


@app.patch("/set-name")
def set_name(
        payload: NewUserName,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
        ):
    try:
        token = credentials.credentials
        decoded_jwt = decode_jwt(token=token)
        user_email = decoded_jwt.get("email")
        return {
            "status": "success",
            "UserInfo": patch_user_name(db, payload.new_user_name, user_email)
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }


@app.patch("/upload-avatar")
def upload_avatar(
        avatar: UploadFile = File(...),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
        ):
    try:
        if not avatar.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return HTTPException(status_code=400, detail="Неподдерживаемый формат файла")
        token = credentials.credentials
        payload = decode_jwt(token=token)
        user_email = payload.get("email")
        return {
            "status": "success",
            "UserInfo": patch_user_avatar(db, user_email, avatar)
            }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }


@app.post("/reset-password")
def request_for_reset_password(payload: UserBase, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, payload.email)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not found")
    hashed_reset_code = generate_and_send_verify_code(payload.email)
    post_reset_code(db, hashed_reset_code, db_user)
    return {"status": "success"}


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
        return {"status": "success"}
    else:
        return HTTPException(status_code=400, detail="Reset code is not correct")


@app.get("/authorization-via-jwt")
def authorization_via_jwt(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token)
        user_email = payload.get("email")
        return {
            "status": "success",
            "UserInfo": get_user_via_jwt(db, user_email)
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }

# Возможно нужно реализовать подтверждение пользователя через код, который будет отправлен на почту
@app.patch("/change-email")
def change_email(
        new_user_email: NewUserEmail,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token)
        user_email = payload.get("email")
        return {
            "status": "success",
            "updateInformation": path_user_email(db, user_email, new_user_email.new_user_email)
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }
