# app/api/teachers.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd

from app.api.dependencies import get_db, get_current_user
from app.db.session import engine

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.get("/effectiveness")
def get_teacher_effectiveness(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = """
    SELECT 
        t.id AS teacher_id,
        t.name AS teacher_name,
        COUNT(s.id) AS student_count,
        AVG(sc.score) AS avg_score,
        AVG(tf.feedback_score) AS avg_feedback
    FROM teachers t
    LEFT JOIN teacher_feedback tf ON t.id = tf.teacher_id
    LEFT JOIN classes c ON t.id = c.teacher_id
    LEFT JOIN students s ON c.id = s.class_id
    LEFT JOIN student_scores sc ON s.id = sc.student_id
    GROUP BY t.id, t.name
    """
    df = pd.read_sql(query, engine)
    corr = df["avg_feedback"].corr(df["avg_score"]) if "avg_feedback" in df and "avg_score" in df else None
    return {
        "teacher_effectiveness": df.to_dict(orient="records"),
        "correlation_feedback_vs_score": round(corr, 2) if corr else "Insufficient data"
    }
