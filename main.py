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


@app.post("/create-category")
def create_category(
        new_category: CategoryDto,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token)
        user_id = uuid.UUID(payload["sub"])
        return {
            "status": "success",
            "NewCategoryInfo": post_category(db, user_id, new_category.name)
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }


@app.patch("/edit-category")
def edit_category(
    category: CategoryDtoPatch,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token)
        user_id = payload["sub"]
        return {
            "status": "success",
            "EditCategoryInfo": patch_category(db, uuid.UUID(user_id), category.name, category.new_name)
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }
    except HTTPException as error:
        raise error


@app.delete("/delete-category")
def remove_category(
        payload: CategoryDto,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        decoded_token = decode_jwt(token=token)
        user_id = decoded_token["sub"]
        return {
            "status": "success",
            "DeleteInfo": delete_category(db, uuid.UUID(user_id), payload.name)
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }
    except HTTPException as error:
        raise error


@app.post("/create-project")
def create_project(
        payload: ProjectDtoWithCategoryId,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        decoded_token = decode_jwt(token=token)
        return {
            "status": "success",
            "ProjectInfo": post_project(db, payload.name, uuid.UUID(decoded_token["sub"]), uuid.UUID(payload.category_id))
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }


@app.patch("/upload-project-avatar")
def upload_project_avatar(
        project_name: str,
        avatar: UploadFile = File(...),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    try:
        if not avatar.filename.lower().endswith((".png", ".jpg", "jpeg")):
            return HTTPException(status_code=400, detail="Неподдерживаемый формат файла")
        token = credentials.credentials
        payload = decode_jwt(token=token)
        return {
            "status": "success",
            "message": set_project_avatar(db, project_name, uuid.UUID(payload["sub"]), payload["email"], avatar)
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }
    except HTTPException as error:
        raise error


@app.patch("/edit-project")
def edit_project(
    new_project: ProjectDtoPatch,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = decode_jwt(token)
        return {
            "status": "success",
            "details": patch_project(db, new_project.name, new_project.new_name, uuid.UUID(payload.get("sub")))
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }
    except HTTPException as error:
        raise error


@app.delete("/remove-project")
def remove_project(
        project: ProjectDto,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token)
        return {
            "status": "success",
            "message": delete_project(db, uuid.UUID(payload.get("sub")), project.name)
        }
    except ExpiredSignatureError:
        return {
            "status": "error",
            "details": "token expired"
        }


@app.post("/create-task")
def create_task(

):
