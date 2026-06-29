"""Reports Router — Generate and download reports."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, timezone
import uuid, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from schemas import ReportRequest, ReportResponse
from auth import get_current_user_id, require_role

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    req: ReportRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Generate a report (daily/weekly/monthly/executive)."""
    from services.report_generator import ReportGenerator
    generator = ReportGenerator()
    try:
        file_path = await generator.generate(db, req.report_type, req.start_date,
                                              req.end_date, req.location_id, req.format)
        return ReportResponse(
            report_id=str(uuid.uuid4()), report_type=req.report_type,
            file_path=file_path, generated_at=datetime.now(timezone.utc)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.get("/download/{filename}")
async def download_report(filename: str, user_id: int = Depends(get_current_user_id)):
    """Download a generated report file."""
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_reports")
    file_path = os.path.join(reports_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(file_path, filename=filename)
