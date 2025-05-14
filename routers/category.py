from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session

from database.get_database import get_db
from schemas.category_schemas import CategoryDtoCreate, CategoryDtoPatch, CategoryDtoDelete
from schemas.response.category import CategoryResponse
from service.category_service import CategoryService


router = APIRouter(
    prefix="/category",
    tags=["Category"]
)

http_bearer = HTTPBearer()


@router.post("/create-category", response_model=CategoryResponse)
def create_category(
        new_category: CategoryDtoCreate,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return CategoryService(db=db).create_category(new_category=new_category, credentials=credentials)


@router.get("/get-all-categories")
def get_all_categories(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return CategoryService(db).get_all_category(credentials)


@router.patch("/edit-category", response_model=CategoryResponse)
def edit_category(
    category: CategoryDtoPatch,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    return CategoryService(db=db).edit_category(category=category, credentials=credentials)


@router.delete("/delete-category", response_model=CategoryResponse)
def remove_category(
        payload: CategoryDtoDelete,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return CategoryService(db=db).remove_category(payload=payload, credentials=credentials)
