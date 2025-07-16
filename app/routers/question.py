from typing import List, Union
from fastapi import APIRouter, HTTPException, Query, status, Depends
from app.database import get_session
from sqlmodel import Session
from app.services import question
from app.schemas.question import Question, QuestionCreate, QuestionUpdate, QuestionWithAnswers

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

@router.get("/", response_model=List[Question])
async def get_all(session: Session = Depends(get_session)):
    questions = question.get_all_questions(session)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions

@router.get("/search", response_model=List[Question])
async def search(
    partial_title: str, 
    session: Session = Depends(get_session)
):
    results = question.search_question(session, partial_title)
    if not results:
        raise HTTPException(status_code=404, detail="No questions found")
    return results

@router.get("/{id}", response_model=Union[Question, QuestionWithAnswers])
async def get_by_id(
    id: int, 
    include_answers: bool = Query(False, description="Include answers in response"),
    session: Session = Depends(get_session)
):
    result = question.get_question_by_id(session, id, include_answers)
    if result is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return result

@router.post("/", response_model=Question)
async def create(
    question_data: QuestionCreate, 
    session: Session = Depends(get_session)
):
    try:
        new_question = question.create_question(session, question_data)
        return new_question
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{id}", response_model=Question)
async def update(
    id: int, 
    update_data: QuestionUpdate,
    session: Session = Depends(get_session)
):
    try:
        updated_question = question.update_question(session, id, update_data)
        if updated_question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return updated_question
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    session: Session = Depends(get_session)
):
    success = question.delete_question(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Deleted successfully"}
