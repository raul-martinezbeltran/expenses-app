from fastapi import FastAPI
from backend.app.routers.expense.service import router as expense_router
from backend.app.routers.user.service import router as user_router
from backend.log_config import logger

tags_metadata = [
    {"name": "expenses", "description": "Operations with expenses"},
    {"name": "users", "description": "Operations with users"},
]

app = FastAPI(openapi_url="/api/v1/", openapi_tags=tags_metadata)

app.include_router(expense_router)
app.include_router(user_router)
