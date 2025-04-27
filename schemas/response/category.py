from pydantic import BaseModel
from schemas.category_schemas import CategoryDto


class CategoryResponse(BaseModel):
    status: str
    category: CategoryDto


class CategoriesResponse(BaseModel):
    status: str
    categories: list[CategoryDto]
