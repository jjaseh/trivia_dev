from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select, func
from app.models.answer import Answer as AnswerModel
from app.models.question import Question
from app.schemas.answer import Answer, AnswerCreate, AnswerUpdate

def get_all_answers(session: Session) -> List[Answer]:
    db_answers = session.exec(select(AnswerModel)).all()
    return [Answer.model_validate(q) for q in db_answers]

def get_answer_by_id(session: Session, id: int) -> Optional[Answer]:
    db_answer = session.get(AnswerModel, id)
    if db_answer is None:
        return None
    return Answer.model_validate(db_answer)

def search_answer(session: Session, partial_text: str) -> List[Answer]:
    statement = select(AnswerModel).where(
        func.lower(AnswerModel.text).contains(partial_text.lower())
    )
    db_answers = session.exec(statement)
    return [Answer.model_validate(q) for q in db_answers]

def create_answer(session: Session, data: AnswerCreate) -> Answer:
    question = session.get(Question, data.question_id)
    if not question:
       raise HTTPException(status_code=404, detail="Question does not exist")
    new_answer = AnswerModel(**data.model_dump())
    session.add(new_answer)
    session.commit()
    session.refresh(new_answer)
    return Answer.model_validate(new_answer)

def create_answers(session: Session, data: List[AnswerCreate]) -> List[Answer]:
    question_ids = set(ans.question_id for ans in data)
    if len(question_ids) > 1:
        raise HTTPException(status_code=400, detail="All answers must belong to the same question.")
    question_id = next(iter(question_ids))
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question does not exist")
    correct_answers = [ans for ans in data if ans.is_correct]
    if len(correct_answers) != 1:
        raise HTTPException(status_code=400, detail="Exactly one answer must be marked as correct.")
    new_answers = [AnswerModel(**item.model_dump()) for item in data]
    session.add_all(new_answers)
    session.commit()
    for ans in new_answers: 
        session.refresh(ans)
    return [Answer.model_validate(q) for q in new_answers]

def update_answer(session: Session, id: int, data: AnswerUpdate) -> Optional[Answer]:
    answer = session.get(AnswerModel, id)
    if not answer:
        return None
    if not data.question_id is None:
        question = session.get(Question, data.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question does not exist")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(answer, key, value)
    session.add(answer)
    session.commit()
    session.refresh(answer)
    return Answer.model_validate(answer)

def delete_answer(session: Session, id: int) -> bool:
    answer = session.get(AnswerModel, id)
    if not answer:
        return False
    session.delete(answer)
    session.commit()
    return True