import uuid

from fastapi import HTTPException
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials

from schemas.category_schemas import CategoryDtoCreate, CategoryDtoPatch, CategoryDtoDelete
from schemas.response.category import CategoryResponse
from service_utils.category import post_category, get_all_categories, patch_category, delete_category
from utils import decode_jwt


class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_category(
            self,
            new_category: CategoryDtoCreate,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = uuid.UUID(payload["sub"])
            return CategoryResponse(
                status="success",
                category=post_category(self.db, user_id, new_category.name)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def get_all_category(
            self,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = uuid.UUID(payload["sub"])
            return {
                "status": "success",
                "Categories": get_all_categories(self.db, user_id)
            }
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def edit_category(
            self,
            category: CategoryDtoPatch,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            payload = decode_jwt(token=token)
            user_id = payload["sub"]
            return CategoryResponse(
                status="success",
                category=patch_category(self.db, uuid.UUID(user_id), category.category_id, category.new_name)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error

    def remove_category(
            self,
            payload: CategoryDtoDelete,
            credentials: HTTPAuthorizationCredentials
    ):
        try:
            token = credentials.credentials
            decoded_token = decode_jwt(token=token)
            user_id = decoded_token["sub"]
            return CategoryResponse(
                status="success",
                category=delete_category(self.db, uuid.UUID(user_id), payload.category_id)
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")
        except HTTPException as error:
            raise error
