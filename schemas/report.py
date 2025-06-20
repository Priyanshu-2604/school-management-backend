# app/schemas/report.py

from pydantic import BaseModel
from typing import Optional, List

class KPIReport(BaseModel):
    total_revenue: float
    attendance_percent: float
    avg_student_score: float

class TeacherEffectivenessItem(BaseModel):
    teacher_id: int
    teacher_name: str
    student_count: int
    avg_score: Optional[float]
    avg_feedback: Optional[float]

class TeacherEffectivenessReport(BaseModel):
    teacher_effectiveness: List[TeacherEffectivenessItem]
    correlation_feedback_vs_score: Optional[float]
