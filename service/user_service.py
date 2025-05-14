from fastapi import UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials

from schemas.response.status import StatusResponse
from schemas.response.user import UserResponse
from schemas.user_schemas import NewUserName, UserSetAvatar, UserBase, UserNewPassword
from service_utils.user import patch_user_name, patch_user_avatar, get_user_by_email, post_reset_code, get_reset_code, \
    patch_user_password, delete_reset_code, get_user_via_jwt, path_user_email
from utils import decode_jwt, generate_and_send_verify_code, match_hash, get_password_hash
import uuid
from jwt import ExpiredSignatureError
from datetime import datetime
from service_utils.attachment import get_attachment_info


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def set_name(
            self,
            payload: NewUserName,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_jwt = decode_jwt(token=token)
            user_id = uuid.UUID(decoded_jwt["sub"])
            return UserResponse(
                status="success",
                info_about_user=patch_user_name(self.db, payload.new_user_name, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def set_avatar(
            self,
            payload: UserSetAvatar,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            user_id = uuid.UUID(decoded_token.get("sub"))
            attachment = get_attachment_info(self.db, payload.avatar_id)
            print(attachment.path)
            return UserResponse(
                status="success",
                info_about_user=patch_user_avatar(self.db, user_id, payload.avatar_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def request_for_reset_password(
            self,
            payload: UserBase
    ):
        db_user = get_user_by_email(self.db, payload.email)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        hashed_reset_code = generate_and_send_verify_code(payload.email)
        post_reset_code(self.db, hashed_reset_code, db_user)
        return StatusResponse(
            status="success"
        )

    def confirm_the_reset(
            self,
            payload: UserNewPassword,
    ):
        found_code = get_reset_code(self.db, payload.email)
        if found_code is None:
            raise HTTPException(status_code=400, detail="Reset code for this user not found")
        if match_hash(payload.verify_code, found_code.hashed_code):
            if datetime.now().time() > found_code.expiration_time:
                raise HTTPException(status_code=400, detail="The verify code has expired")
            patch_user_password(self.db, found_code.user, get_password_hash(payload.new_password))
            delete_reset_code(self.db, found_code)
            return StatusResponse(
                status="success"
            )
        else:
            return HTTPException(status_code=400, detail="Reset code is not correct")

    def authorization_via_jwt(self, credentials: HTTPAuthorizationCredentials):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = uuid.UUID(payload.get("sub"))
            return UserResponse(
                status="success",
                info_about_user=get_user_via_jwt(self.db, user_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def change_email(
            self,
            new_user_email: UserBase,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = payload.get("sub")
            return UserResponse(
                status="success",
                info_about_user=path_user_email(self.db, user_id, new_user_email.email)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
