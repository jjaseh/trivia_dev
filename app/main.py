from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import test, category, question
from app.database import create_db_and_tables
from app.models import category as categoryModel, question as questionModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(test.router)
app.include_router(category.router)
app.include_router(question.router)