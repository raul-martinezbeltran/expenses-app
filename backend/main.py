from fastapi import FastAPI
from backend.app.routers.expense.service import router as expense_router
from backend.app.routers.user.service import router as user_router


app = FastAPI(openapi_url="/api/v1")

app.include_router(expense_router)
app.include_router(user_router)