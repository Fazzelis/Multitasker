from fastapi import HTTPException
from sqlalchemy.orm import Session

from service_utils.user import get_user_by_email, post_user
from schemas.response.auth import AuthorizationRegistrationResponse
from schemas.token_schemas import TokenInfo
from schemas.user_schemas import UserCreateAndAuthorization
from utils import get_password_hash, encode_jwt, match_hash


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user: UserCreateAndAuthorization):
        if len(user.password) < 8 or len(user.password) > 16:
            raise HTTPException(status_code=422, detail="Password does not pass validation")
        db_user = get_user_by_email(self.db, user.email)
        if db_user is not None:
            raise HTTPException(status_code=409, detail="Email already registered")
        user.password = get_password_hash(user.password)
        created_user = post_user(self.db, user)

        jwt_payload = {
            "sub": str(created_user.id)
        }
        token = encode_jwt(payload=jwt_payload)
        token_info = TokenInfo(
            token=token,
            token_type="Bearer"
        )
        return AuthorizationRegistrationResponse(
            status="success",
            token_info=token_info
        )

    def authorization(self, user: UserCreateAndAuthorization):
        db_user = get_user_by_email(self.db, user.email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if match_hash(user.password, db_user.hashed_password):
            jwt_payload = {
                "sub": str(db_user.id)
            }
            token = encode_jwt(payload=jwt_payload)
            token_info = TokenInfo(
                token=token,
                token_type="Bearer"
            )
            return AuthorizationRegistrationResponse(
                status="success",
                token_info=token_info
            )
        else:
            raise HTTPException(status_code=401, detail="Login or password is not correct")
