from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.get_database import get_db
from schemas.response.status import StatusResponse
from schemas.response.user import UserResponse
from schemas.user_schemas import NewUserName, UserSetAvatar, UserBase, UserNewPassword
from service.user_service import UserService

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


@router.patch("/set-avatar", response_model=UserResponse)
def set_avatar(
        payload: UserSetAvatar,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return UserService(db).set_avatar(payload, credentials)


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
