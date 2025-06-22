from fastapi import FastAPI
from routers import test, category

app = FastAPI()

app.include_router(test.router)
app.include_router(category.router)
