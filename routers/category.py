from fastapi import APIRouter
from fastapi.security import HTTPBearer
from jwt import ExpiredSignatureError
from database.get_database import get_db
from crud.category import *
from crud.user import *
from utils import *
from schemas.category_schemas import *
from service.category_service import CategoryService
from schemas.response.category import *


router = APIRouter(
    prefix="/category",
    tags=["Category"]
)

http_bearer = HTTPBearer()


@router.post("/create-category", response_model=CategoryResponse)
def create_category(
        new_category: CategoryDto,
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
    category: CategoryDtoPatchDelete,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    return CategoryService(db=db).edit_category(category=category, credentials=credentials)


@router.delete("/delete-category", response_model=CategoryResponse)
def remove_category(
        payload: CategoryDtoPatchDelete,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        db: Session = Depends(get_db)
):
    return CategoryService(db=db).remove_category(payload=payload, credentials=credentials)
