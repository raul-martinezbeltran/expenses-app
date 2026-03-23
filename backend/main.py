from fastapi import FastAPI
from backend.app.routers.expense.service import router as expense_router
from backend.app.routers.user.service import router as user_router
from backend.log_config import logger
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {"name": "expenses", "description": "Operations with expenses"},
    {"name": "users", "description": "Operations with users"},
]

app = FastAPI(
    openapi_url="/api/v1/openapi.json",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expense_router)
app.include_router(user_router)
