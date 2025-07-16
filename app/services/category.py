from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy import func
from app.models.category import Category as CategoryModel
from app.schemas.category import Category, CategoryCreate, CategoryUpdate, CategoryWithQuestions
from typing import List, Optional

def get_all_categories(session: Session) -> List[Category]:
    db_categories = session.exec(select(CategoryModel)).all()
    return [Category.model_validate(c) for c in db_categories]

def get_category_by_id(session: Session, id: int, include_questions: bool = False) -> Optional[BaseModel]:
    db_category = session.get(CategoryModel, id)
    if db_category is None:
        return None
    if include_questions:
        return CategoryWithQuestions.model_validate(db_category)
    return Category.model_validate(db_category)

def search_category(session: Session, partial_name: str) -> List[Category]:
    statement = select(CategoryModel).where(
        func.lower(CategoryModel.name).contains(partial_name.lower())
    )
    db_categories = session.exec(statement)
    return [Category.model_validate(c) for c in db_categories]

def create_category(session: Session, data: CategoryCreate) -> Optional[Category]:
    new_category = CategoryModel(**data.model_dump())
    find_by_name_statement = select(CategoryModel).where(
        func.lower(CategoryModel.name) == new_category.name.lower()
    )
    same_name_category = session.exec(find_by_name_statement).first()
    if same_name_category:
        return None
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return Category.model_validate(new_category)

def update_category(session: Session, id: int, data: CategoryUpdate) -> Optional[Category]:
    category = session.get(CategoryModel, id)
    if not category:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    session.add(category)
    session.commit()
    session.refresh(category)
    return Category.model_validate(category)

def delete_category_by_id(session: Session, id: int) -> bool:
    category = session.get(CategoryModel, id)
    if not category:
        return False
    session.delete(category)
    session.commit()
    return True