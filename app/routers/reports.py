from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, require_roles
from app.services.report_service import ReportService
from app.schemas.reports import DashboardResponse

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    """Admin dashboard — user counts, resource stats, active/overdue loans, top penalty users."""
    return ReportService(db).get_dashboard()


@router.post("/send-overdue-reminders")
async def send_overdue_reminders(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    """
    Sends overdue reminder emails to all users whose active loans have passed fecha_limite.
    Emails are sent in the background — returns immediately with a count.
    """
    from app.services.email_service import send_loan_overdue_email

    overdue_items = ReportService(db).get_overdue_loans_for_reminder()
    for item in overdue_items:
        correo = item.pop("correo")
        background_tasks.add_task(send_loan_overdue_email, correo, item)

    return {
        "message": f"Queued {len(overdue_items)} overdue reminder email(s).",
        "total": len(overdue_items),
    }
