from fastapi import FastAPI
from backend.app.routers.expense import service

app = FastAPI()

app.include_router(service.router)