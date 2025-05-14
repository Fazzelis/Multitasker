from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exists
from uuid import UUID
from models import Category
from schemas.category_schemas import CategoryDto


def post_category(db: Session, user_id: UUID, category_name: str):
    exist_category = db.query(exists().where(
        Category.name == category_name,
        Category.user_id == user_id
    )).scalar()

    if exist_category:
        raise HTTPException(status_code=409, detail="Категория уже существует")
    new_category = Category(
        name=category_name,
        user_id=user_id
    )
    db.add(new_category)
    db.commit()
    return CategoryDto(
        category_id=new_category.id,
        name=new_category.name
    )


def get_all_categories(
        db: Session,
        user_id: UUID
) -> list:
    return db.query(Category).filter(Category.user_id == user_id).all()


def patch_category(db: Session, user_id: UUID, category_id: UUID, new_category_name: str):
    category = db.query(Category).filter(Category.user_id == user_id).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = new_category_name
    db.add(category)
    db.commit()
    db.refresh(category)
    return CategoryDto(
        category_id=category.id,
        name=new_category_name
    )


def delete_category(db: Session, user_id: UUID, category_id: UUID):
    category = db.query(Category).filter(Category.user_id == user_id).filter(Category.id == category_id).one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return CategoryDto(
        category_id=category.id,
        name=category.name
    )
