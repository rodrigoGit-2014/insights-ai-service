import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base

class InsightCache(Base):
    __tablename__ = "insight_cache"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    insight_type = Column(String(50), nullable=False)
    request_hash = Column(String(32), nullable=False, index=True)
    request_params = Column(JSONB, nullable=False)
    response_data = Column(JSONB, nullable=False)
    token_usage = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
