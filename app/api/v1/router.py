from fastapi import APIRouter
from app.api.v1.endpoints import insights, reports, chat

api_router = APIRouter()
api_router.include_router(insights.router)
api_router.include_router(reports.router)
api_router.include_router(chat.router)
