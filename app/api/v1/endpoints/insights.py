import asyncio
import json
import logging
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.api.auth_deps import get_current_user, get_raw_token, TokenData
from app.schemas.insights import InsightRequest
from app.services.insight_service import InsightService
from app.core.cache import cache

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/insights/generate")
async def generate_insights(
    request: InsightRequest,
    current_user: TokenData = Depends(get_current_user),
    token: str = Depends(get_raw_token),
):
    service = InsightService()
    result = await service.generate_insight(
        auth_token=token,
        company_id=str(current_user.company_id),
        insight_type=request.insight_type,
        start_date=str(request.start_date) if request.start_date else None,
        end_date=str(request.end_date) if request.end_date else None,
        department_id=request.department_id,
        section_id=request.section_id,
    )
    return result

@router.post("/insights/generate/stream")
async def generate_insights_stream(
    request: InsightRequest,
    current_user: TokenData = Depends(get_current_user),
    token: str = Depends(get_raw_token),
):
    service = InsightService()

    async def stream():
        gen = service.generate_insight_stream(
            auth_token=token,
            company_id=str(current_user.company_id),
            insight_type=request.insight_type,
            start_date=str(request.start_date) if request.start_date else None,
            end_date=str(request.end_date) if request.end_date else None,
            department_id=request.department_id,
            section_id=request.section_id,
        )
        async for chunk in gen:
            yield chunk

    return StreamingResponse(stream(), media_type="text/plain")

@router.delete("/insights/cache")
async def clear_cache(current_user: TokenData = Depends(get_current_user)):
    count = cache.delete_pattern(f"v1:insight:*{current_user.company_id}*")
    return {"cleared": count}
