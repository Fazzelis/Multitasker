from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.get_database import get_db
from schemas.user_schemas import *
from service.auth_service import AuthService
from schemas.response.auth import *

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register-user", response_model=AuthorizationRegistrationResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register_user(user)


@router.post("/authorization", response_model=AuthorizationRegistrationResponse)
def authorization(user: UserAuthorization, db: Session = Depends(get_db)):
    return AuthService(db).authorization(user)
