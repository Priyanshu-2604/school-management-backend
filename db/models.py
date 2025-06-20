# app/db/models.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    class_id = Column(String)

    transactions = relationship("Transaction", back_populates="student")
    scores = relationship("StudentScore", back_populates="student")
    attendance = relationship("Attendance", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    feedbacks = relationship("TeacherFeedback", back_populates="teacher")
    classes = relationship("Class", back_populates="teacher")

class Class(Base):
    __tablename__ = "classes"
    id = Column(String, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    teacher = relationship("Teacher", back_populates="classes")
    students = relationship("Student", backref="class_")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    amount = Column(Float)
    transaction_date = Column(Date)
    payment_type = Column(String)
    payment_method = Column(String)
    status = Column(String)

    student = relationship("Student", back_populates="transactions")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date)
    status = Column(String)

    student = relationship("Student", back_populates="attendance")

class StudentScore(Base):
    __tablename__ = "student_scores"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    score = Column(Float)
    exam_date = Column(Date)

    student = relationship("Student", back_populates="scores")

class TeacherFeedback(Base):
    __tablename__ = "teacher_feedback"
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    feedback_score = Column(Float)

    teacher = relationship("Teacher", back_populates="feedbacks")
