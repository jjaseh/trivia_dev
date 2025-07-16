from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class AnswerBase(BaseModel):
    text: str = Field(..., min_length=1)
    is_correct: bool

class AnswerCreate(AnswerBase):
    question_id: int

class BulkAnswerCreate(BaseModel):
    answers: List[AnswerCreate]

    model_config = {"arbitrary_types_allowed": True}

class AnswerUpdate(BaseModel):
    text: Optional[str] = Field(default=None, min_length=1)
    is_correct: Optional[bool] = None
    question_id: Optional[int] = None

class Answer(AnswerBase):
    id: int
    question_id: int

    model_config = ConfigDict(from_attributes=True)

class AnswerInQuestion(AnswerBase):
    
    model_config = ConfigDict(from_attributes=True)