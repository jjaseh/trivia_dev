from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import get_session
from sqlmodel import Session
from app.services import answer
from app.schemas.answer import Answer, AnswerCreate, AnswerUpdate

router = APIRouter(
    prefix="/answers",
    tags=["Answers"]
)

@router.get("/", response_model=List[Answer])
async def get_all(session: Session = Depends(get_session)):
    answers = answer.get_all_answers(session)
    if not answer:
        raise HTTPException(status_code=404, detail="No answers found")
    return answers

@router.get("/search", response_model=List[Answer])
async def search(
    partial_text: str, 
    session: Session = Depends(get_session)
):
    results = answer.search_answer(session, partial_text)
    if not results:
        raise HTTPException(status_code=404, detail="No answers found")
    return results

@router.get("/{id}", response_model=Answer)
async def get_by_id(
    id: int, 
    session: Session = Depends(get_session)
):
    result = answer.get_answer_by_id(session, id)
    if result is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return result

@router.post("/", response_model=Answer, status_code=status.HTTP_201_CREATED)
async def create(
    answer_data: AnswerCreate, 
    session: Session = Depends(get_session)
):
    try:
        new_answer = answer.create_answer(session, answer_data)
        return new_answer
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/bulk", response_model=List[Answer], status_code=status.HTTP_201_CREATED)
async def bulk(
    data: List[AnswerCreate], 
    session: Session = Depends(get_session)
):
    if not data:
        raise HTTPException(status_code=400, detail="Answer list is empty")
    new_answers = answer.create_answers(session, data)
    return new_answers

@router.patch("/{id}", response_model=Answer)
async def update(
    id: int, 
    update_data: AnswerUpdate,
    session: Session = Depends(get_session)
):
    try:
        updated_answer = answer.update_answer(session, id, update_data)
        if updated_answer is None:
            raise HTTPException(status_code=404, detail="Answer not found")
        return updated_answer
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(
    id: int,
    session: Session = Depends(get_session)
):
    success = answer.delete_answer(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"message": "Deleted successfully"}
