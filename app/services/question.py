from typing import List, Optional
from sqlmodel import Session, select, func
from app.models.question import Question as QuestionModel
from app.schemas.question import Question, QuestionCreate, QuestionUpdate
from app.models.category import Category

def get_all_questions(session: Session) -> List[Question]:
    db_questions = session.exec(select(QuestionModel)).all()
    return [Question.model_validate(q) for q in db_questions]

def get_question_by_id(session: Session, id: int) -> Optional[Question]:
    db_question = session.get(QuestionModel, id)
    if db_question is None:
        return None
    return Question.model_validate(db_question)

def search_question(session: Session, partial_title: str) -> List[Question]:
    statement = select(QuestionModel).where(
        func.lower(QuestionModel.title).contains(partial_title.lower())
    )
    db_questions = session.exec(statement)
    return [Question.model_validate(q) for q in db_questions]

def create_question(session: Session, data: QuestionCreate) -> Question:
    category = session.get(Category, data.category_id)
    if not category:
        raise ValueError("Category does not exist")
    new_question = QuestionModel(**data.model_dump())
    session.add(new_question)
    session.commit()
    session.refresh(new_question)
    return Question.model_validate(new_question)

def update_question(session: Session, id: int, data: QuestionUpdate) -> Optional[Question]:
    question = session.get(QuestionModel, id)
    if not question:
        return None
    if not data.category_id is None:
        category = session.get(Category, data.category_id)
        if not category:
            raise ValueError("Category does not exist")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(question, key, value)
    session.add(question)
    session.commit()
    session.refresh(question)
    return Question.model_validate(question)

def delete_question(session: Session, id: int) -> bool:
    question = session.get(QuestionModel, id)
    if not question:
        return False
    session.delete(question)
    session.commit()
    return True