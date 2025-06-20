# app/services/ml_models.py

import pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from app.db.models import Student, StudentScore, Transaction
from sqlalchemy.orm import Session
import numpy as np

class MLModelManager:
    def __init__(self):
        self.performance_model = None
        self.dropout_model = None
        self.revenue_model = None

    def train_performance_model(self, db: Session):
        students = db.query(Student).all()
        data = []
        for student in students:
            scores = [s.score for s in student.scores]
            if not scores:
                continue
            avg_score = np.mean(scores)
            attendance = student.attendance
            if not attendance:
                continue
            attendance_rate = sum(1 for a in attendance if a.status == "present") / len(attendance)
            data.append({"score": avg_score, "attendance": attendance_rate})

        df = pd.DataFrame(data)
        if len(df) < 5:
            return

        X = df[["attendance"]]
        y = df["score"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = LinearRegression().fit(X_train, y_train)
        self.performance_model = model

    def train_dropout_model(self, db: Session):
        students = db.query(Student).all()
        data = []
        for student in students:
            scores = [s.score for s in student.scores]
            if not scores:
                continue
            avg_score = np.mean(scores)
            attendance = student.attendance
            if not attendance:
                continue
            attendance_rate = sum(1 for a in attendance if a.status == "present") / len(attendance)
            dropped = student.is_dropout
            data.append({"score": avg_score, "attendance": attendance_rate, "dropped": int(dropped)})

        df = pd.DataFrame(data)
        if len(df["dropped"].unique()) < 2:
            return

        X = df[["score", "attendance"]]
        y = df["dropped"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = LogisticRegression().fit(X_train, y_train)
        self.dropout_model = model

    def train_revenue_model(self, db: Session):
        transactions = db.query(Transaction).all()
        data = [{"amount": t.amount, "month": t.transaction_date.month} for t in transactions]
        df = pd.DataFrame(data)
        if len(df) < 5:
            return

        X = df[["month"]]
        y = df["amount"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = LinearRegression().fit(X_train, y_train)
        self.revenue_model = model

    def predict_student_score(self, attendance_rate: float) -> float:
        if not self.performance_model:
            return 0
        return self.performance_model.predict([[attendance_rate]])[0]

    def predict_dropout_risk(self, score: float, attendance_rate: float) -> float:
        if not self.dropout_model:
            return 0
        return float(self.dropout_model.predict_proba([[score, attendance_rate]])[0][1])

    def predict_revenue(self, month: int) -> float:
        if not self.revenue_model:
            return 0
        return self.revenue_model.predict([[month]])[0]
