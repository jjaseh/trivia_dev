from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_correct: bool
    
    question_id: int = Field(default=None, foreign_key="question.id")
    question: Optional["Question"] = Relationship(back_populates="answers")