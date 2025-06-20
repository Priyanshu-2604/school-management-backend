# app/api/management.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.dependencies import get_db, require_role
from app.db.models import Attendance, StudentScore, Transaction

router = APIRouter(prefix="/management", tags=["Management"])

@router.get("/kpis")
def get_management_kpis(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "principal"]))
):
    kpi = {}

    kpi["total_revenue"] = round(db.query(func.sum(Transaction.amount)).scalar() or 0, 2)
    total = db.query(Attendance).count()
    present = db.query(Attendance).filter(Attendance.status == "present").count()
    kpi["attendance_percent"] = round((present / total) * 100, 2) if total else 0
    kpi["avg_student_score"] = round(db.query(func.avg(StudentScore.score)).scalar() or 0, 2)

    return kpi
