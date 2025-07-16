from typing import List, Union
from fastapi import APIRouter, HTTPException, Query, status, Depends
from app.database import get_session
from sqlmodel import Session
from app.services import category
from app.schemas.category import Category, CategoryCreate, CategoryUpdate, CategoryWithQuestions

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/", response_model=List[Category])
async def get_all(session: Session = Depends(get_session)):
    categories = category.get_all_categories(session)
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return categories

@router.get("/search", response_model=List[Category])
async def search(
    partial_name: str, 
    session: Session = Depends(get_session)
):
    results = category.search_category(session, partial_name)
    if not results:
        raise HTTPException(status_code=404, detail="No categories found")
    return results

@router.get("/{id}", response_model=Union[Category, CategoryWithQuestions])
async def get_by_id(
    id: int, 
    include_questions: bool = Query(False, description="Include questions in response"),
    session: Session = Depends(get_session)
):
    result = category.get_category_by_id(session, id, include_questions)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return result

@router.post("/", response_model=Category)
async def create(
    category_data: CategoryCreate, 
    session: Session = Depends(get_session)
):
    new_category = category.create_category(session, category_data)
    if new_category is None:
        raise HTTPException(status_code=409, detail="A category with the same name already exists")
    return new_category

@router.patch("/{id}", response_model=Category)
async def update(
    id: int, 
    update_data: CategoryUpdate,
    session: Session = Depends(get_session)
):
    updated_category = category.update_category(session, id, update_data)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    session: Session = Depends(get_session)
):
    success = category.delete_category_by_id(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Deleted successfully"}
