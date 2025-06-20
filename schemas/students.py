# app/schemas/students.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

class StudentOverview(BaseModel):
    id: int
    name: str
    class_id: str
    avg_score: Optional[float]
    attendance_rate: Optional[float]
    last_seen: Optional[date]

    class Config:
        orm_mode = True

class StudentPerformance(BaseModel):
    id: int
    name: str
    class_id: str
    avg_score: Optional[float]
    total_exams: int
    attendance_rate: Optional[float]
    total_attendance_records: int
    last_exam_date: Optional[date]

    class Config:
        orm_mode = True
