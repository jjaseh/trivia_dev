from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from app.schemas.question import QuestionInCategory

class CategoryBase(BaseModel):
    name: str 
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    name: str = Field(..., min_length=2)

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    questions: List[QuestionInCategory] = []

    model_config = ConfigDict(from_attributes=True)