from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.get_database import get_db
from schemas.response.auth import AuthorizationRegistrationResponse
from schemas.user_schemas import UserCreateAndAuthorization
from service.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register-user", response_model=AuthorizationRegistrationResponse)
async def register(user: UserCreateAndAuthorization, db: Session = Depends(get_db)):
    return AuthService(db).register_user(user)


@router.post("/authorization", response_model=AuthorizationRegistrationResponse)
async def authorization(user: UserCreateAndAuthorization, db: Session = Depends(get_db)):
    return AuthService(db).authorization(user)
