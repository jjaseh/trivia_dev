from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from app.schemas.answer import AnswerInQuestion

class QuestionBase(BaseModel): 
    title: str = Field(..., min_length=10)
    difficulty: Optional[str] = Field(default="medium", pattern="^(easy|medium|hard)$")
    explanation: Optional[str] = None
    category_id: int

class QuestionCreate(QuestionBase): 
    pass

class QuestionUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=10)
    difficulty: Optional[str] = Field(default=None, pattern="^(easy|medium|hard)$")
    explanation: Optional[str] = None
    category_id: Optional[int] = None

class QuestionInCategory(BaseModel):
    title: str
    difficulty: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class Question(QuestionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class QuestionWithAnswers(QuestionBase):
    answers: List[AnswerInQuestion] = []
    model_config = ConfigDict(from_attributes=True)