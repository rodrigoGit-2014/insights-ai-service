from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class ReportRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    department_id: Optional[str] = None
    section_id: Optional[str] = None
    format: str = Field(default="pdf", pattern="^(pdf|docx|pptx)$")
    report_type: str = Field(default="executive", pattern="^(executive|cross_selling|patterns)$")

class ReportJobResponse(BaseModel):
    job_id: UUID
    status: str
    message: str
    created_at: datetime

class ReportStatusResponse(BaseModel):
    job_id: UUID
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
