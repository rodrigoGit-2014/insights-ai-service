import uuid
import enum
from sqlalchemy import Column, String, Integer, Text, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"

class ReportJob(Base):
    __tablename__ = "report_jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    status = Column(SQLEnum(ReportStatus, name="report_status", values_callable=lambda x: [e.value for e in x]),
                    nullable=False, default=ReportStatus.PENDING)
    format = Column(String(10), nullable=False)
    report_type = Column(String(50), nullable=False)
    file_path = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
