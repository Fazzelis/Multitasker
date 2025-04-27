from fastapi import File, APIRouter
from fastapi.security import HTTPBearer
from jwt import ExpiredSignatureError
from database.get_database import get_db
from crud.user import *
from utils import *
from schemas.user_schemas import *
from service.user_service import UserService
from schemas.response.user import *
from schemas.response.avatar import *
from schemas.response.status import *


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

http_bearer = HTTPBearer()


@router.patch("/set-name", response_model=UserResponse)
def set_name(
        payload: NewUserName,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
        ):
    return UserService(db).set_name(payload=payload, credentials=credentials)


@router.patch("/upload-avatar", response_model=AvatarResponse)
def upload_avatar(
        avatar: UploadFile = File(...),
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
        ):
    return UserService(db=db).upload_avatar(avatar=avatar, credentials=credentials)


@router.post("/reset-password", response_model=StatusResponse)
def request_for_reset_password(payload: UserBase, db: Session = Depends(get_db)):
    return UserService(db=db).request_for_reset_password(payload=payload)


@router.post("/confirm-reset-password", response_model=StatusResponse)
def confirm_the_reset(payload: UserNewPassword, db: Session = Depends(get_db)):
    return UserService(db=db).confirm_the_reset(payload=payload)


@router.get("/authorization-via-jwt", response_model=UserResponse)
def authorization_via_jwt(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(get_db)):
    return UserService(db=db).authorization_via_jwt(credentials=credentials)


@router.patch("/change-email", response_model=UserResponse)
def change_email(
        new_user_email: UserBase,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return UserService(db=db).change_email(new_user_email=new_user_email, credentials=credentials)
