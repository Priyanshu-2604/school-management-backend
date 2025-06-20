# app/db/seed.py

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import User, Student, Teacher, Class, Transaction, Attendance, StudentScore, TeacherFeedback
from app.core.security import get_password_hash

def seed_data(db: Session):
    # Users
    admin = User(username="admin", email="admin@example.com", hashed_password=get_password_hash("admin123"), role="admin")
    principal = User(username="principal", email="principal@example.com", hashed_password=get_password_hash("principal123"), role="principal")
    db.add_all([admin, principal])
    
    # Teachers and Classes
    teacher = Teacher(name="John Smith")
    class_ = Class(id="10A", teacher=teacher)
    db.add(class_)
    
    # Students
    student = Student(name="Alice", class_id="10A")
    db.add(student)

    # Transactions
    txn = Transaction(
        student=student,
        amount=1500.0,
        transaction_date=datetime.now().date(),
        payment_type="tuition",
        payment_method="cash",
        status="completed"
    )
    db.add(txn)

    # Attendance
    for i in range(5):
        db.add(Attendance(
            student=student,
            date=datetime.now().date() - timedelta(days=i),
            status="present" if i % 2 == 0 else "absent"
        ))

    # Scores
    db.add(StudentScore(
        student=student,
        subject="Math",
        score=88.0,
        exam_date=datetime.now().date() - timedelta(days=10)
    ))

    # Feedback
    db.add(TeacherFeedback(teacher=teacher, feedback_score=4.5))

    db.commit()
