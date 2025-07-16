from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    difficulty: Optional[str] = None
    explanation: Optional[str] = None

    category_id: int = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="questions")
    answers: List["Answer"] = Relationship(back_populates="question")