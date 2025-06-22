from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from services import category
from schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/", response_model=List[Category])
async def get_all():
    return category.get_all_categories()

@router.get("/search", response_model=List[Category])
async def search_categories(partial_name: str):
    results = category.get_categories_by_partial_name(partial_name)
    if not results:
        raise HTTPException(status_code=404, detail="No categories found")
    return results

@router.get("/{id}", response_model=Category)
async def get_by_id(id: int):
    result = category.get_category_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return result

@router.post("/", response_model=Category)
async def create(category_data: CategoryCreate):
    new_category = category.create_category(category_data)
    return new_category

@router.patch("/{id}", response_model=Category)
async def update(id: int, update_data: CategoryUpdate):
    updated_category = category.update_category(id, update_data)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int):
    success = category.delete_category_by_id(id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
