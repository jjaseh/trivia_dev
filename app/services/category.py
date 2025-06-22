from schemas.category import Category, CategoryCreate, CategoryUpdate
from typing import List, Optional

_categories: List[Category] = []

def get_all_categories() -> List[Category]:
    return _categories

def get_categories_by_partial_name(partial_name: str) -> List[Category]:
    results = []
    for category in _categories:
        if partial_name.lower() in category.name.lower():
            results.append(category)
    return results

def get_category_by_id(id: int) -> Optional[Category]:
    for category in _categories:
        if category.id == id:
            return category
    return None

def create_category(data: CategoryCreate) -> Category:
    next_id = len(_categories) + 1
    new_category = Category(id=next_id, **data.model_dump())
    _categories.append(new_category)
    return new_category

def update_category(id: int, data: CategoryUpdate) -> Optional[Category]:
    for index, category in enumerate(_categories):
        if category.id == id:
            updated_data = data.model_dump(exclude_unset = True)
            updated_category = category.model_copy(update=updated_data)
            _categories[index] = updated_category
            return updated_category
    return None

def delete_category_by_id(id: int) -> bool:
    for index, category in enumerate(_categories):
        if category.id == id:
            del _categories[index]
            return True
    return False