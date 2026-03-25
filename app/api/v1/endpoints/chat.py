import logging
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.api.auth_deps import get_current_user, get_raw_token, TokenData
from app.schemas.chat import ChatRequest
from app.services.insight_service import InsightService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat")
async def chat_with_ai(
    request: ChatRequest,
    current_user: TokenData = Depends(get_current_user),
    token: str = Depends(get_raw_token),
):
    service = InsightService()

    async def stream():
        gen = service.generate_chat_stream(
            auth_token=token,
            company_id=str(current_user.company_id),
            messages=[m.model_dump() for m in request.messages],
            start_date=request.start_date,
            end_date=request.end_date,
        )
        async for chunk in gen:
            yield chunk

    return StreamingResponse(stream(), media_type="text/plain")
