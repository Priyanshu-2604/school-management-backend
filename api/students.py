# app/api/students.py

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

from app.api.dependencies import get_db, get_current_user
from app.db.models import Student, StudentScore, Attendance
from app.db.session import engine

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/performance")
def get_student_performance(
    class_id: str = Query(None),
    subject: str = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = """
    SELECT 
        s.id, s.name, s.class_id,
        AVG(sc.score) as avg_score,
        COUNT(sc.id) as total_exams,
        AVG(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as attendance_rate,
        COUNT(a.id) as total_attendance_records,
        MAX(sc.exam_date) as last_exam_date
    FROM students s
    LEFT JOIN student_scores sc ON s.id = sc.student_id
    LEFT JOIN attendance a ON s.id = a.student_id
    WHERE 1=1
    """

    params = {}
    if class_id:
        query += " AND s.class_id = %(class_id)s"
        params["class_id"] = class_id
    if subject:
        query += " AND sc.subject = %(subject)s"
        params["subject"] = subject

    query += " GROUP BY s.id, s.name, s.class_id ORDER BY avg_score DESC"

    df = pd.read_sql(query, engine, params=params)
    return {
        "student_performance": df.to_dict(orient="records"),
        "filters": {"class_id": class_id, "subject": subject}
    }

@router.get("/overview")
def get_student_overview(
    student_name: str = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = db.query(Student).filter(Student.name.ilike(f"%{student_name}%")).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    scores = db.query(StudentScore).filter_by(student_id=student.id).all()
    attendance = db.query(Attendance).filter_by(student_id=student.id).all()

    return {
        "id": student.id,
        "name": student.name,
        "class_id": student.class_id,
        "avg_score": round(np.mean([s.score for s in scores]), 2) if scores else None,
        "attendance_rate": round(sum(1 for a in attendance if a.status == "present") / len(attendance), 2) if attendance else None,
        "last_seen": max(a.date for a in attendance) if attendance else None
    }
