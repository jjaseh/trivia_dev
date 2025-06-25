from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index = True)
    description: Optional[str] = None

    questions: List["Question"] = Relationship(back_populates="category")