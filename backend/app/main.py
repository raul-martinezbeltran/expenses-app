from fastapi import FastAPI
from app.routers import expense

app = FastAPI()

app.include_router(expense.router)