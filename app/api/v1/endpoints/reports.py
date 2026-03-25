import asyncio
import logging
from uuid import UUID
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.api.auth_deps import get_current_user, get_raw_token, TokenData
from app.db.session import get_db
from app.schemas.reports import ReportRequest, ReportJobResponse, ReportStatusResponse
from app.services.report_service import ReportService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/reports/generate")
async def generate_report(
    request: ReportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    token: str = Depends(get_raw_token),
):
    service = ReportService(db)
    job = service.create_job(current_user.company_id, request.format, request.report_type)

    background_tasks.add_task(
        _run_report, job.id, token, request.start_date, request.end_date,
        request.department_id, request.section_id,
    )

    return ReportJobResponse(
        job_id=job.id,
        status=job.status.value,
        message="Report generation started",
        created_at=job.created_at,
    )

async def _run_report(job_id, token, start_date, end_date, department_id, section_id):
    from app.services.report_service import ReportService
    service = ReportService.__new__(ReportService)
    await service.process_report(job_id, token, start_date, end_date, department_id, section_id)

@router.get("/reports/{job_id}/status")
def get_report_status(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    service = ReportService(db)
    job = service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportStatusResponse(
        job_id=job.id,
        status=job.status.value,
        error_message=job.error_message,
        created_at=job.created_at,
        completed_at=job.completed_at,
    )

@router.get("/reports/{job_id}/download")
def download_report(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    service = ReportService(db)
    job = service.get_job(job_id)
    if not job or job.status.value != "completed" or not job.file_path:
        raise HTTPException(status_code=404, detail="Report not ready")
    import os
    filename = os.path.basename(job.file_path)
    media_types = {"pdf": "application/pdf", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"}
    return FileResponse(job.file_path, filename=filename, media_type=media_types.get(job.format, "application/octet-stream"))
